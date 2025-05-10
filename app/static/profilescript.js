document.getElementById('search-button').addEventListener('click', function () {
    const searchQuery = document.getElementById('search-input').value.trim();
    const searchUrl = this.getAttribute('data-search-url'); // Get the URL from the data attribute
    // Make sure the input is not blank before hitting the search button
    if (searchQuery) {
        // send POST request to the server
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
            friendContainer.innerHTML = ''; // Clear previous results

            if (data.length > 0) {
                data.forEach(user => {
                    const friendCard = `
                        <div class="friend-card">
                            <img src="/static/images/default_profile_pic.png" alt="Profile Picture" class="profile-pic">
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