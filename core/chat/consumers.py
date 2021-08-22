from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from core.room.models import Room


def _get_room_name(public_id):

    room = Room.objects.get_object_by_public_id(public_id)

    return room.name


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self, **kwargs):
        room_name = ''
        url_route = self.scope.get('url_route')

        url_route_kwargs = url_route.get('kwargs')

        room_id = url_route_kwargs.get('room_id')

        try:
            room_name = await sync_to_async(_get_room_name, thread_sensitive=True)(public_id=room_id)
            if room_name is None:
                await self.close()

        except Exception as e:
            await self.close()

        self.room_group_name = room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        message = receive_dict["message"]

        action = receive_dict['action']

        if action in ['new-offer', 'new-answer']:
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict
                }
            )
            return

        receive_dict['message']['receiver_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict': receive_dict
            }
        )

    async def send_sdp(self, event):
        receive_dict = event["receive_dict"]

        await self.send(
                text_data=json.dumps(receive_dict)
            )
