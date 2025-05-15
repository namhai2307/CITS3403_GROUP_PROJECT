function showForm(formID) {
    document.querySelectorAll(".form-box").forEach(form => {
        form.classList.remove("active");
    });
    document.getElementById(formID).classList.add("active")
}

document.addEventListener('DOMContentLoaded', function(){
    const monthYear = document.getElementById("month-year");
    const daysContainer = document.getElementById("days");
    
    const months = [
        "January", 
        "February", 
        "March", 
        "April", 
        "May", 
        "June", 
        "July", 
        "August", 
        "September", 
        "October", 
        "November", 
        "December"
    ];
    let currentDate = new Date();
    let today = new Date();

    // Refresh heatmap data and calendar
    function refreshEventDurationsAndCalendar() {
        fetch('/api/event_durations')
            .then(res => res.json())
            .then(data => {
                for (const key in window.eventDurations) delete window.eventDurations[key];
                Object.assign(window.eventDurations, data);
                renderCalendar(currentDate);
            });
    }

    // Rendering Calendar
    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const lastDay = new Date(year, month + 1, 0).getDate();

        monthYear.textContent = `${months[month]} ${year}`;
        daysContainer.innerHTML = '';

        // Last month's date
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        for (let i = firstDay; i > 0; i--) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = prevMonthLastDay - i + 1;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }

        // The current month's date
        for (let i = 1; i <= lastDay; i++){
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('day-cell');
            dayDiv.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;

            // Heatmap: Coloring based on eventDurations
            const dateStr = dayDiv.dataset.date;
            const duration = (window.eventDurations && window.eventDurations[dateStr]) ? window.eventDurations[dateStr] : 0;

            
            dayDiv.style.backgroundColor = '';
            dayDiv.style.color = '';

            if (duration === 0) {
                dayDiv.style.backgroundColor = 'white';
            } else if (duration <= 2) {
                dayDiv.style.backgroundColor = '#00ff00';
            } else if (duration <= 4) {
                dayDiv.style.backgroundColor = '#61f100';
            } else if (duration <= 6) {
                dayDiv.style.backgroundColor = '#89e200';
            } else if (duration <= 8) {
                dayDiv.style.backgroundColor = '#a3d200';
            } else if (duration <= 10) {
                dayDiv.style.backgroundColor = '#b6c300';
            } else if (duration <= 12) {
                dayDiv.style.backgroundColor = '#c7b200';
            } else if (duration <= 14) {
                dayDiv.style.backgroundColor = '#d5a100';
            } else if (duration <= 16) {
                dayDiv.style.backgroundColor = '#e28d00';
            } else if (duration <= 18) {
                dayDiv.style.backgroundColor = '#ee7700';
            } else if (duration <= 20) {
                dayDiv.style.backgroundColor = '#f75e00';
            } else if (duration <= 22) {
                dayDiv.style.backgroundColor = '#fd3f00';
            } else if (duration <= 24) {
                dayDiv.style.backgroundColor = '#ff0000';
            } else {
                dayDiv.style.backgroundColor = '#000000';
                dayDiv.style.color = 'white';
            }

            console.log(dateStr, duration, dayDiv.style.backgroundColor);

            // Highlight today
            if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayDiv.classList.add('today');
            }

            // Click on the event: Highlight and load the event
            dayDiv.addEventListener('click', function () {
                document.querySelectorAll('.day-cell').forEach(cell => cell.classList.remove('today'));
                dayDiv.classList.add('today');
                loadEventsForDate(dayDiv.dataset.date);

                // Update the schedule header with the selected date
                const scheduleHeader = document.querySelector('#schedule-section h5');
                const selectedDate = new Date(dayDiv.dataset.date);
                const options = { weekday: 'long', month: 'long', day: 'numeric' };
                const formattedDate = selectedDate.toLocaleDateString('en-US', options);
                scheduleHeader.innerHTML = `<i class="bi bi-list-task me-2"></i>${formattedDate} Schedule`;
            });

            daysContainer.appendChild(dayDiv);
        }
    }

    // Get the currently selected date
    function getSelectedDate() {
        return document.querySelector('.day-cell.today')?.dataset.date ||
            new Date().toISOString().split('T')[0];
    }

    // List of rendering events
    function renderEventList(events) {
        const container = document.getElementById('today-events');
        container.innerHTML = events.map(event => `
            <div class="event-card mb-3 p-2 border rounded" data-event-id="${event.id}">
                <div class="d-flex justify-content-between">
                    <strong class="event-title">${event.title}</strong>
                    <small class="text-muted">
                        ${new Date(event.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - 
                        ${new Date(event.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </small>
                </div>
                ${event.description ? `<p class="mt-1 mb-0 small event-description">${event.description}</p>` : ''}
                <div class="event-actions mt-2 text-end">
                    <button class="btn btn-sm btn-outline-primary edit-btn">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-outline-danger delete-btn">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </div>
            </div>
        `).join('') || `<div class="alert alert-info mb-0">No events scheduled</div>`;
    }

    // Edit event
    function handleEditEvent(eventId) {
        const eventCard = document.querySelector(`[data-event-id="${eventId}"]`);
        if (!eventCard) return;

        document.getElementById('edit-event-id').value = eventId;
        document.getElementById('edit-title').value = eventCard.querySelector('.event-title')?.textContent.trim() || '';
        document.getElementById('edit-description').value = eventCard.querySelector('.event-description')?.textContent.trim() || '';

        const timeText = eventCard.querySelector('small.text-muted')?.textContent || '';
        const [start, end] = timeText.split(' - ').map(t => t.trim());
        const todayDate = getSelectedDate();

        document.getElementById('edit-start-time').value = `${todayDate}T${start}`;
        document.getElementById('edit-end-time').value = `${todayDate}T${end}`;
        document.getElementById('edit-privacy-level').value = 'private';

        const modal = new bootstrap.Modal(document.getElementById('editEventModal'));
        modal.show();
    }

    // Delete Event
    function handleDeleteEvent(eventId) {
        if (confirm('Are you sure to delete this event?')) {
            fetch(`/api/events/${eventId}`, { 
                method: 'DELETE',
                headers: { 'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content }
            }).then(response => {
                if (response.ok) {
                    loadEventsForDate(getSelectedDate());
                    refreshEventDurationsAndCalendar();
                } else {
                    console.error('Failed to delete event:', response.statusText);
                }
            }).catch(console.error);
        }
    }

    // Load an event from a certain day
    window.loadEventsForDate = function (date) {
        fetch(`/api/events/${date}`)
            .then(response => response.json())
            .then(renderEventList)
            .catch(console.error);
    };

    // Event delegation: Handling edit and delete buttons
    document.addEventListener('click', function (e) {
        const eventCard = e.target.closest('[data-event-id]');
        if (!eventCard) return;

        if (e.target.closest('.edit-btn')) {
            handleEditEvent(eventCard.dataset.eventId);
        } else if (e.target.closest('.delete-btn')) {
            handleDeleteEvent(eventCard.dataset.eventId);
        }
    });

    // Edit Form Submission
    document.getElementById('editEventForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const eventId = document.getElementById('edit-event-id').value;
        const padSeconds = (datetime) => datetime.length === 16 ? `${datetime}:00` : datetime;
        const updatedData = {
            title: document.getElementById('edit-title').value,
            description: document.getElementById('edit-description').value,
            start_time: padSeconds(document.getElementById('edit-start-time').value),
            end_time: padSeconds(document.getElementById('edit-end-time').value),
            privacy_level: document.getElementById('edit-privacy-level').value
        };

        fetch(`/api/events/${eventId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify(updatedData)
        }).then(response => {
            if (response.ok) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('editEventModal'));
                modal.hide();
                loadEventsForDate(getSelectedDate());
                refreshEventDurationsAndCalendar();
            }
        })
    });

    // Rendering Calendar and Events of the Day
    renderCalendar(currentDate);
    const todayDate = new Date();
    const todayStr = `${todayDate.getFullYear()}-${String(todayDate.getMonth() + 1).padStart(2, '0')}-${String(todayDate.getDate()).padStart(2, '0')}`;
    loadEventsForDate(todayStr);

    // Month switching
    document.getElementById('prev').addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });
    document.getElementById('next').addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });
});


