document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Connect to the SocketIO server
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');
    const friendSelector = document.getElementById('friend-selector');

    let room = null; // Room will be dynamically set based on the selected friend
    let selectedFriendId = null;

    // Join a chat room
    function joinRoom(newRoom) {
        if (room) {
            // Leave the current room
            socket.emit('leave_room', { room: room, username: username });
        }
        room = newRoom;
        socket.emit('join_room', { room: room, username: username });
        messagesContainer.innerHTML = ''; // Clear previous messages
    }

    // Fetch messages between the current user and the selected friend
    function fetchMessages(friendId) {
        fetch(`/messages/${friendId}`)
            .then(response => response.json())
            .then(messages => {
                messagesContainer.innerHTML = ''; // Clear previous messages
                messages.forEach(msg => {
                    const messageElement = document.createElement('div');
                    const senderName = msg.sender_id === currentUserId ? 'You' : friendSelector.options[friendSelector.selectedIndex].text;
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
                messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to the bottom
            })
            .catch(error => console.error('Error fetching messages:', error));
    }

    // Listen for chat history
    socket.on('chat_history', (messages) => {
        messages.forEach((msg) => {
            const messageElement = document.createElement('div');
            messageElement.textContent = `${msg.username}: ${msg.message} (${msg.timestamp})`;
            messagesContainer.appendChild(messageElement);
        });
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to the bottom
    });

    // Listen for incoming messages
    socket.on('receive_message', (data) => {
        const messageElement = document.createElement('div');
        const senderName = data.username === username ? 'You' : data.username;
        const timestamp = new Date().toLocaleString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
            month: 'short',
            day: 'numeric',
        });
        messageElement.textContent = `${senderName}: ${data.message} (${timestamp})`;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to the bottom
    });

    // Listen for user join/leave events
    socket.off('user_joined'); // Remove any existing listener
    socket.on('user_joined', (data) => {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username} joined the chat.`;
        messageElement.classList.add('text-muted');
        messagesContainer.appendChild(messageElement);
    });

    socket.off('user_left'); // Remove any existing listener
    socket.on('user_left', (data) => {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username} left the chat.`;
        messageElement.classList.add('text-muted');
        messagesContainer.appendChild(messageElement);
    });

    // Handle friend selection
    friendSelector.addEventListener('change', () => {
        selectedFriendId = friendSelector.value;
        if (selectedFriendId) {
            joinRoom(`room_${selectedFriendId}`); // Use a unique room name for each friend
            fetchMessages(selectedFriendId);
        }
    });

    // Handle message form submission
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
                        messageInput.value = ''; // Clear the input field
                        fetchMessages(selectedFriendId); // Refresh messages
                    }
                })
                .catch(error => console.error('Error sending message:', error));
        } else {
            alert('Please select a friend and type a message.');
        }
    });

    // Leave the room when the user navigates away
    window.addEventListener('beforeunload', () => {
        if (room) {
            socket.emit('leave_room', { room: room, username: username });
        }
    });
});