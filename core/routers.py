from rest_framework.routers import SimpleRouter
from core.room.viewsets import RoomViewSet

routes = SimpleRouter()

# ROOM
routes.register(r'room', RoomViewSet, basename='room')



urlpatterns = [
    *routes.urls
]