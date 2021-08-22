console.log("Working.")

var pcConfig = {
    'iceServers': [
        {
            'urls': ['stun:35.180.71.59:3478'],
            'username': 'test',
            'credential': 'test123',
            'credentialType': 'password',
        },
        {
            'urls': ['turn:35.180.71.59:3478'],
            'username': 'test',
            'credential': 'test123',
            'credentialType': 'password',
        }
    ]
};

const NEW_PEER = 'new-peer';

let mapPeers = {};

console.log(mapPeers)

let usernameInput = document.querySelector('#username');
let roomIdInput = document.querySelector('#roomId')
let btnJoin = document.querySelector('#btn-join');

let username;

let roomId;

let webSocket;

function webSocketOnMessage(event) {
    let parseData = JSON.parse(event.data);

    let peerUsername = parseData.peer;

    let action = parseData.action;

    if(username === peerUsername){
        return;
    }

    let receiverChannelName = parseData['message']['receiver_channel_name'];
    if (action === NEW_PEER) {
        createOffer(peerUsername, receiverChannelName);
        return;
    }

    if (action === 'new-offer') {
        let offer = parseData['message']['sdp'];

        createAnswer(offer, peerUsername, receiverChannelName)

        return;

    }

    if (action === 'new-answer') {
        let answer = parseData['message']['sdp'];

        console.log(answer)

        let peer = mapPeers[peerUsername][0];

        peer.setRemoteDescription(answer);

        return;

    }


}

btnJoin.addEventListener('click', () => {
    username = usernameInput.value;
    roomId = roomIdInput.value;
    if( username === '' || roomId === '') {
        return;
    }

    usernameInput.value = '';
    usernameInput.disabled = true;
    usernameInput.style.visibility = 'hidden';

    roomIdInput.value = '';
    roomIdInput.disabled = true;
    roomIdInput.style.visibility = 'hidden';

    btnJoin.disabled = true;
    btnJoin.style.visibility = 'hidden';

    let usernameLabel = document.querySelector('#label-username');
    usernameLabel.innerHTML = username;

    let loc = window.location;

    let wsStart = 'ws://';

    if(loc.protocol === 'https:') {
        wsStart = 'wss://'
    }

    let endPoint = wsStart + loc.host + loc.pathname + 'room/506abf286f17488786237f2d8dc009ca/';
    webSocket = new WebSocket(endPoint);

    webSocket.addEventListener('open', (e) => {
        console.log('Connection Opened');

       sendSignal('new-peer', {})
    })

    webSocket.addEventListener('message', webSocketOnMessage)
    webSocket.addEventListener('close', (e) => {
        console.log('Connection Closed')
    })
    webSocket.addEventListener('error', (e) => {
        console.log('Error occured.')

    })

});

let localStream = new MediaStream();

const constraints = {
    'video': true,
    'audio': true
};

const localVideo = document.querySelector('#local-video');


const btnToggleAudio = document.querySelector('#btn-toggle-audio');

const btnToggleVideo = document.querySelector('#btn-toggle-video');

let userMedia = navigator.mediaDevices.getUserMedia(constraints).then(
    stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;

        let audioTracks = stream.getAudioTracks()

        let videoTracks = stream.getVideoTracks();

        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;

        btnToggleAudio.addEventListener('click', () => {
            audioTracks[0].enabled = !audioTracks[0].enabled;

            if(audioTracks[0].enabled){
                btnToggleAudio.innerHTML = 'Audio muted';

                return;
            }

            btnToggleAudio.innerHTML = 'Audio Unmute';
        })

        btnToggleVideo.addEventListener('click', () => {
            videoTracks[0].enabled = !videoTracks[0].enabled;

            if(videoTracks[0].enabled){
                btnToggleVideo.innerHTML = 'Video off';

                return;
            }

            btnToggleVideo.innerHTML = 'Video on';
        })
    }
).catch( error => {
    console.log({'Error': error})
})



function sendSignal(action, message) {
    let jsonStr = JSON.stringify(
            {
                'peer': username,
                'action': action,
                'message': message
            }
        )

    webSocket.send(jsonStr)
}

function createOffer(peerUsername, receiverChannelName){
    let peer = new RTCPeerConnection({iceServers: pcConfig.iceServers});

    addLocalTracks(peer);

    let dc = peer.createDataChannel('channel');

    dc.addEventListener('open', () => {
        console.log('Connection opened.');
    })

    dc.addEventListener('message', dcOnMessage);

    let remoteVideo = createVideo(peerUsername); // Define the function

    setOnTrack(peer, remoteVideo); //Define the function

    mapPeers[peerUsername] = [peer, dc];

    peer.addEventListener('iceconnectionstatechange', () => {
        let iceconnectionState = peer.iceConnectionState;

        if (iceconnectionState === "failed" || iceconnectionState === 'disconnected'
            || iceconnectionState === 'closed'
        ) {
            delete  mapPeers[peerUsername];

            if (iceconnectionState !== 'closed') {
                peer.close();
            }

            removeVideo(remoteVideo);
        }
    })

    peer.addEventListener('icecandidate', (event) => {
        if(event.candidate) {
            console.log('New Ice candidate');
            return;

        }

        sendSignal('new-offer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiverChannelName

        });
    })

    peer.createOffer().then(
        res => peer.setLocalDescription(res)
    ).then(() => {
            console.log('Local description working.')
    })
}



function createAnswer(offer, peerUsername, receiverChannelName) {
    let peer = new RTCPeerConnection({iceServers: pcConfig.iceServers});

    addLocalTracks(peer);

    let remoteVideo = createVideo(peerUsername); // Define the function

    setOnTrack(peer, remoteVideo); //Define the function

    peer.addEventListener('datachannel', e => {
        peer.dc = e.channel;

        peer.dc.addEventListener('open', () => {
        console.log('Connection opened.');
        })

        peer.dc.addEventListener('message', dcOnMessage);

        mapPeers[peerUsername] = [peer, peer.dc]
    })

    peer.addEventListener('iceconnectionstatechange', () => {
        let iceconnectionState = peer.iceConnectionState;

        if (iceconnectionState === "failed" || iceconnectionState === 'disconnected'
            || iceconnectionState === 'closed'
        ) {
            delete  mapPeers[peerUsername];

            if (iceconnectionState !== 'closed') {
                peer.close();
            }

            removeVideo(remoteVideo);
        }
    })

    peer.addEventListener('icecandidate', (event) => {
        if(event.candidate) {
            console.log('New Ice candidate');
            return;

        }

        sendSignal('new-answer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiverChannelName

        });
    })

    peer.setRemoteDescription(offer).then(
        () => {
            console.log('Remote Description Good!', peerUsername);

            return peer.createAnswer();
        }
    ).then(
        r => {
            peer.setLocalDescription(r);
        }
    )
}

function addLocalTracks(peer) {
    localStream.getTracks().forEach( track => (
        peer.addTrack(track, localStream)
    ));

    return;
}

let messageList = document.querySelector('#message-list');

function dcOnMessage(event) {
    let message = event.data;

    let li = document.createElement('li');

    li.appendChild(document.createTextNode(message));

    messageList.appendChild(li);
}

function createVideo(peerUsername) {
    let videoContainer = document.querySelector('#video-container');

    let remoteVideo = document.createElement('video');

    remoteVideo.id = peerUsername + '-video';

    remoteVideo.autoplay = true;

    remoteVideo.playsinline = true;

    remoteVideo.style = "border: black solid 1px;";

    let videoWrapper = document.createElement('div');

    videoContainer.appendChild(videoWrapper);

    videoWrapper.appendChild(remoteVideo);

    return remoteVideo;

}

function setOnTrack(peer, remoteVideo) {
    let remoteStream = new MediaStream();

    remoteVideo.srcObject = remoteStream;
    console.log(remoteVideo)

    peer.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    });

}

function removeVideo(video) {
    let videoWrapper = video.parentNode;

    videoWrapper.parentNode.removeChild(videoWrapper)
}

let btnSendMsg = document.querySelector('#btn-send-msg');

let messageInput = document.querySelector('#msg');

btnSendMsg.addEventListener('click', sendMsgOnClick);

function sendMsgOnClick() {
    let message = messageInput.value;

    let li = document.createElement('li');

    li.appendChild(document.createTextNode('Me: ' + message));

    messageList.appendChild(li);

    let dataChannels = getDataChannels();

    message = username + ': ' + message;

    dataChannels.forEach(dc => {
        dc.send(message);
    });

    messageInput.value = '';


}

function getDataChannels() {
    let dataChannels = [];

    for (let peerUsername in mapPeers) {
        let peer = mapPeers[peerUsername][1];

        if (peer) {
            dataChannels.push(peer);
        }
    }

    return dataChannels;
}