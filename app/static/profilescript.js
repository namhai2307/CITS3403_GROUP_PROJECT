/**
 * @fileoverview Friend search functionality using AJAX.
 *
 * This script handles user-initiated friend searches via a button click.
 * It sends the search query to a backend endpoint using a POST request,
 * receives a list of matching users, and dynamically renders user "friend cards"
 * into the DOM. If no users are found, it displays an appropriate message.
 *
 * Features:
 * - Fetch-based AJAX request with JSON payload
 * - Dynamic DOM manipulation based on server response
 * - Graceful handling of empty results and errors
 *
 * Dependencies:
 * - Assumes presence of elements with IDs: 'search-button', 'search-input', 'friend-container'
 * - Uses Bootstrap classes for styling (e.g. 'btn', 'text-center')
 *
*/

document.getElementById('search-button').addEventListener('click', function () {
    const searchQuery = document.getElementById('search-input').value.trim();
    const searchUrl = this.getAttribute('data-search-url'); 
    if (searchQuery) {
        fetch(searchUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ search_query: searchQuery }),
        })

        .then(response => response.json())
        .then(data => {
            const friendContainer = document.getElementById('friend-container');
            friendContainer.innerHTML = ''; 

            if (data.length > 0) {
                data.forEach(user => {
                    const friendCard = `
                        <div class="friend-card">
                            <img src="/static/images/default_profile_pic.png" alt="Profile Picture" class="profile-pic" />
                            <h3 class="friend-name">${user.username}</h3>
                            <p class="friend-title">${user.email}</p>
                            <button class="btn btn-primary">Add Friend</button>
                        </div>
                    `;
                    friendContainer.innerHTML += friendCard;
                });
            } else {
                friendContainer.innerHTML = '<p class="text-center mt-4">No user found. Try another username.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

function validatePassword() {
    const newPassword = document.getElementById('newPassword').value;
    const confPassword = document.getElementById('confPassword').value;

    if (newPassword !== confPassword) {
        alert('New passwords do not match.');
        return false;
    }

    if (newPassword.length < 8) {
        alert('Password must be at least 8 characters long.');
        return false;
    }

    return true;
}

function validateEmail() {
    const newEmail = document.getElementById('newEmail').value;
    const confEmail = document.getElementById('confEmail').value;

    if (newEmail !== confEmail) {
        alert('Emails do not match.');
        return false;
    }

    return true;
}