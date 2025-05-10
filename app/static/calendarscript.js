function showForm(formID) {
    document.querySelectorAll(".form-box").forEach(form => form.classList.remove("active"));
    document.getElementById(formID).classList.add("active")
}

document.addEventListener('DOMContentLoaded', function () {
    const monthYear = document.getElementById("month-year");
    const daysContainer = document.getElementById("days");
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    const todayEventsContainer = document.getElementById('today-events'); // Container for today's events

    const urlParams = new URLSearchParams(window.location.search);
    const urlDate = urlParams.get('date');

    let currentDate = urlDate ? new Date(urlDate) : new Date();

    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const lastDay = new Date(year, month + 1, 0).getDate();

        monthYear.textContent = `${months[month]} ${year}`;
        daysContainer.innerHTML = '';

        // Previous month's dates
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        for (let i = firstDay; i > 0; i--) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = prevMonthLastDay - i + 1;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }

        // Current month's dates
        for (let i = 1; i <= lastDay; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('day-number');

            // Highlight Logic
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            const duration = eventDurations[dateStr] || 0;

            // Assign data-duration attribute
            dayDiv.setAttribute('data-duration', duration);

            // Apply heatmap colors based on event duration
            if (duration === 0) {
                dayDiv.style.backgroundColor = 'white'; // No events
            } else if (duration <= 2) {
                dayDiv.style.backgroundColor = '#ffcccc'; // Light red for few events
            } else if (duration <= 5) {
                dayDiv.style.backgroundColor = '#ff6666'; // Medium red for more events
            } else {
                dayDiv.style.backgroundColor = '#cc0000'; // Dark red for most events
            }

            // Add click event
            dayDiv.addEventListener('click', function () {
                const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                fetchEventsForDay(dateStr); // Fetch and display events for the selected day
            });

            daysContainer.appendChild(dayDiv);
        }

        // Next month's dates
        const nextMonthStartDay = 7 - new Date(year, month + 1, 0).getDay() - 1;
        for (let i = 1; i <= nextMonthStartDay; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }
    }

    // Fetch and display events for a specific day
    function fetchEventsForDay(dateStr) {
        // Update the URL with the selected date
        const url = new URL(window.location);
        url.searchParams.set('date', dateStr);
        window.history.pushState({}, '', url);

        // Update the schedule header on the frontend
        const scheduleHeader = document.querySelector('#schedule-section h5');
        const newDate = new Date(dateStr);
        // Format the date as "Weekday, Month day" (using en-US locale here)
        const options = { weekday: 'long', month: 'long', day: 'numeric' };
        const formattedDate = newDate.toLocaleDateString('en-US', options);
        scheduleHeader.innerHTML = `<i class="bi bi-list-task me-2"></i>${formattedDate} Schedule`;

        // Clear the today's events container
        const todayEventsContainer = document.getElementById('today-events');
        todayEventsContainer.innerHTML = '';

        // Fetch events for the selected day
        fetch(`/api/events?date=${dateStr}`)
            .then(response => response.json())
            .then(data => {
                if (data.events && data.events.length > 0) {
                    data.events.forEach(event => {
                        const eventDiv = document.createElement('div');
                        eventDiv.classList.add('event-card', 'mb-3', 'p-2', 'border', 'rounded');
                        eventDiv.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <strong>${event.title}</strong>
                                <small class="text-muted">${event.start_time} - ${event.end_time}</small>
                            </div>
                            ${event.description ? `<p class="mt-1 mb-0 small">${event.description}</p>` : ''}
                        `;
                        todayEventsContainer.appendChild(eventDiv);
                    });
                } else {
                    // Clear container if no events found
                    todayEventsContainer.innerHTML = '';
                }
            })
            .catch(error => console.error('Error fetching events:', error));
    }

    // Previous button event listener - toggle previous month
    prevButton.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    // Next button event listener - toggle next month
    nextButton.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    // Initial render
    renderCalendar(currentDate);
});
