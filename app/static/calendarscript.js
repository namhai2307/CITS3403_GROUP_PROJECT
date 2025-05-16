/**
 * @fileoverview Interactive calendar UI with event heatmap and date-based event retrieval.
 *
 * This script dynamically renders a monthly calendar view with heatmap-style coloring
 * based on event duration. It enables users to navigate between months and fetch
 * daily events on click. The schedule for a selected day is retrieved from the backend
 * via a RESTful API and rendered dynamically.
 *
 * Features:
 * - Month navigation (previous/next)
 * - Dynamic day cell rendering with faded edge days from adjacent months
 * - Heatmap visualization of event density using eventDurations object
 * - AJAX-based fetch of events for a selected day
 * - URL update to reflect selected date
 * - Graceful fallback when an editing form is active
 *
 * Dependencies:
 * - A global object `eventDurations` containing event duration per date (in minutes or hours)
 * - HTML elements with IDs: 'month-year', 'days', 'prev', 'next', 'today-events', 'schedule-section', 'editEventForm'
 * - Bootstrap icons and utility classes for styling
 *
 */

function showForm(formID) {
    document.querySelectorAll(".form-box").forEach(form => form.classList.remove("active"));
    document.getElementById(formID).classList.add("active")
}

document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('editEventForm')) {
        return;
    }

    const monthYear = document.getElementById("month-year");
    const daysContainer = document.getElementById("days");
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    const todayEventsContainer = document.getElementById('today-events');

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

        const prevMonthLastDay = new Date(year, month, 0).getDate();
        for (let i = firstDay; i > 0; i--) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = prevMonthLastDay - i + 1;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }

        for (let i = 1; i <= lastDay; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('day-number');

            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            const duration = eventDurations[dateStr] || 0;
    
            dayDiv.setAttribute('data-duration', duration);

            if (duration === 0) {
                dayDiv.style.backgroundColor = 'white'; 
            } else if (duration <= 2) {
                dayDiv.style.backgroundColor = '#ffcccc'; 
            } else if (duration <= 5) {
                dayDiv.style.backgroundColor = '#ff6666';
            } else {
                dayDiv.style.backgroundColor = '#cc0000'; 
            }

            dayDiv.addEventListener('click', function () {
                const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                fetchEventsForDay(dateStr); 
            });

            daysContainer.appendChild(dayDiv);
        }

        const nextMonthStartDay = 7 - new Date(year, month + 1, 0).getDay() - 1;
        for (let i = 1; i <= nextMonthStartDay; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }
    }

    function fetchEventsForDay(dateStr) {
        
        if (document.getElementById('editEventForm')) {
            return;
        }

        const url = new URL(window.location);
        url.searchParams.set('date', dateStr);
        window.history.pushState({}, '', url);

        const scheduleHeader = document.querySelector('#schedule-section h5');
        const newDate = new Date(dateStr);
        const options = { weekday: 'long', month: 'long', day: 'numeric' };
        const formattedDate = newDate.toLocaleDateString('en-US', options);
        scheduleHeader.innerHTML = `<i class="bi bi-list-task me-2"></i>${formattedDate} Schedule`;

        const todayEventsContainer = document.getElementById('today-events');
        todayEventsContainer.innerHTML = '';

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
                    todayEventsContainer.innerHTML = '';
                }
            })
            .catch(error => console.error('Error fetching events:', error));
    }

    prevButton.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextButton.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    renderCalendar(currentDate);
});
