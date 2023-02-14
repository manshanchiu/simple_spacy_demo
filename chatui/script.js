const socket = new WebSocket('ws://localhost:8000/ws');


socket.onmessage = function(event) {
    const message = event.data;
    console.log(message)
    const jm = JSON.parse(message)
    const chat = document.getElementById('chat');
    const p = document.createElement('p');
    const span = document.createElement('span');
    if (isSender(message)) {
        p.className = 'sender';
        span.innerText = 'You';
    } else {
        p.className = 'receiver';
        span.innerText = `Bot: (${parseInt(jm.score * 100)}%)\n`;
    }
    
    p.appendChild(span);
    p.appendChild(document.createTextNode(getMessageText(jm.a)));
    const span2 = document.createElement('span');
    span2.innerText = `\nOriginal Question: ${jm.q}`
    p.appendChild(span2);
    chat.appendChild(p);

    // const div = document.createElement('div');
    // div.className="separator"
    // chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
};

socket.onopen = function(event) {
    console.log('WebSocket is open: ', event);
};

function sendMessage() {
    const input = document.getElementById('message');
    const message = input.value;

    const chat = document.getElementById('chat');
    const p = document.createElement('p');
    const span = document.createElement('span');
    p.className = 'sender';
    span.innerText = 'You';
    p.appendChild(span);
    p.appendChild(document.createTextNode(': ' + getMessageText(message)));
    chat.appendChild(p);
    const div = document.createElement('div');
    div.className="separator"
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    socket.send(message);
    input.value = '';
}

function isSender(message) {
    return message.startsWith('You:');
}

function getMessageText(message) {
    return message.replace(/^You:/, '').trim();
}

const messageInput = document.getElementById('message');

messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage();
    }
  });