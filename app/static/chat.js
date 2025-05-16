/**
 * @fileoverview Real-time chat interface with Socket.IO integration.
 *
 * This script powers a user-to-user messaging interface with live updates,
 * dynamic room switching, and message history retrieval. It uses WebSockets
 * (via Socket.IO) to send and receive real-time messages and events, and 
 * interacts with the server via fetch for message history and persistence.
 *
 * Features:
 * - Automatically joins and leaves chat rooms based on selected friend
 * - Fetches chat history when a new friend is selected
 * - Sends messages both via WebSocket and HTTP POST for persistence
 * - Listens for real-time events: `receive_message`, `user_joined`, `user_left`
 * - Dynamically updates DOM with messages and connection events
 *
 * Dependencies:
 * - Socket.IO (client)
 * - DOM elements with IDs: 'message-form', 'message-input', 'messages', 'friend-selector'
 * - Global variables expected: `username`, `currentUserId`
 *
*/

document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); 
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');
    const friendSelector = document.getElementById('friend-selector');

    let room = null; 
    let selectedFriendId = null;

    function joinRoom(newRoom) {
        if (room) {
            socket.emit('leave_room', { room: room, username: username });
        }
        room = newRoom;
        socket.emit('join_room', { room: room, username: username });
        messagesContainer.innerHTML = '';
    }

    function fetchMessages(friendId) {
        fetch(`/messages/${friendId}`)
            .then(response => response.json())
            .then(messages => {
                messagesContainer.innerHTML = ''; 
                messages.forEach(msg => {
                    const messageElement = document.createElement('div');
                    const senderName = msg.sender_id === parseInt(currentUserId) ? 'You' : msg.sender_username;
                    const timestamp = new Date(msg.timestamp).toLocaleString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: true,
                        month: 'short',
                        day: 'numeric',
                    });

                    messageElement.textContent = `${senderName}: ${msg.content} (${timestamp})`;
                    messagesContainer.appendChild(messageElement);
                });
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            })
            .catch(error => console.error('Error fetching messages:', error));
    }

    socket.on('chat_history', (messages) => {
        messages.forEach((msg) => {
            const messageElement = document.createElement('div');
            messageElement.textContent = `${msg.username}: ${msg.message} (${msg.timestamp})`;
            messagesContainer.appendChild(messageElement);
        });
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });

    socket.on('receive_message', (data) => {
        const messageElement = document.createElement('div');
        const senderName = data.sender_id === parseInt(currentUserId) ? 'You' : data.sender_username;
        const timestamp = new Date(data.timestamp).toLocaleString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
            month: 'short',
            day: 'numeric',
        });

        messageElement.textContent = `${senderName}: ${data.message} (${timestamp})`;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });

    socket.off('user_joined'); 
    socket.on('user_joined', (data) => {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username} joined the chat.`;
        messageElement.classList.add('text-muted');
        messagesContainer.appendChild(messageElement);
    });

    socket.off('user_left'); 
    socket.on('user_left', (data) => {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username} left the chat.`;
        messageElement.classList.add('text-muted');
        messagesContainer.appendChild(messageElement);
    });

    friendSelector.addEventListener('change', () => {
        selectedFriendId = friendSelector.value;
        if (selectedFriendId) {
            joinRoom(`room_${selectedFriendId}`); 
            fetchMessages(selectedFriendId);
        }
    });

    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value;
        const content = messageInput.value;
        if (room && selectedFriendId && content) {
            socket.emit('send_message', { room: room, username: username, message: message });
            fetch('/messages/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ recipient_id: selectedFriendId, content: content })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        messageInput.value = ''; 
                        fetchMessages(selectedFriendId); 
                    }
                })
                .catch(error => console.error('Error sending message:', error));
        } else {
            alert('Please select a friend and type a message.');
        }
    });

    window.addEventListener('beforeunload', () => {
        if (room) {
            socket.emit('leave_room', { room: room, username: username });
        }
    });
});