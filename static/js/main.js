console.log("Working.")

const NEW_PEER = 'new-peer';

let usernameInput = document.querySelector('#username');
let btnJoin = document.querySelector('#btn-join');

let username;

let webSocket;

function webSocketOnMessage(event) {
    let parseData = JSON.parse(event.data);

    let peerUsername = parseData.peer;

    let action = parseData.action;

    if(username === peerUsername){
        return;
    }

    let receiverChannelName = parseData.message.receiver_channel_message;

    if (action === NEW_PEER) {
        createOfferer(peerUsername, receiverChannelName);
    }

    return;

}

btnJoin.addEventListener('click', () => {
    username = usernameInput.value;

    console.log(username)

    if( username === '') {
        return;
    }

    usernameInput.value = '';
    usernameInput.disabled = true;
    usernameInput.style.visibility = 'hidden';

    btnJoin.disabled = true;
    btnJoin.style.visibility = 'hidden';

    let usernameLabel = document.querySelector('#label-username');
    usernameLabel.innerHTML = username;

    let loc = window.location;

    let wsStart = 'ws://';

    if(loc.protocol === 'https:') {
        wsStart = 'wss://'
    }

    let endPoint = wsStart + loc.host + loc.pathname;

    console.log({'endpoint': endPoint})

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

let userMedia = navigator.mediaDevices.getUserMedia(constraints).then(
    stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;

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

function createOfferer(peerUsername, receiverChannelName){
    let peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    let dc = peer.createDataChannel('channel');

    dc.addEventListener('open', () => {
        console.log('Connection opened.');
    })

    dc.addEventListener('message', dcOnMessage);

    let remoteVideo = createVideo(peerUsername);

}


function addLocalTracks(peer) {
    localStream.getTracks().forEach( track => (
        peer.addTrack(tract, localStream)
    ));

    return;
}

let messageList = document.querySelector('message-list');

function dcOnMessage(event) {
    let message = event.data;

    let li = document.createElement('li');

    li.appendChild(document.createTextNode(message));

    messageList.appendChild(li);
}