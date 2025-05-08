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

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const lastDay = new Date(year, month + 1, 0).getDate();

        monthYear.textContent = `${months[month]} ${year}`;
        daysContainer.innerHTML = '';

        //Previous month's dates
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        for (let i = firstDay; i > 0; i--) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = prevMonthLastDay - i + 1;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }

        // Current month's date
        for (let i = 1; i <= lastDay; i++){
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('day-cell');
            dayDiv.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            
            if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayDiv.classList.add('today');
            }
            daysContainer.appendChild(dayDiv);
        }
    }

    function getSelectedDate() {
        return document.querySelector('.day-cell.today')?.dataset.date ||
            new Date().toISOString().split('T')[0];
    }

    // ====================== Event Management Section ======================
    function renderEventList(events) {
        const container = document.getElementById('today-events');
        
        container.innerHTML = events.map(event => `
            <div class="event-card mb-3 p-2 border rounded" data-event-id="${event.id}">
                <div class="d-flex justify-content-between">
                    <strong>${event.title}</strong>
                    <small class="text-muted">
                        ${new Date(event.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - 
                        ${new Date(event.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </small>
                </div>
                ${event.description ? `<p class="mt-1 mb-0 small">${event.description}</p>` : ''}
                <div class="event-actions mt-2 text-end">
                    <button class="btn btn-sm btn-outline-primary edit-event-btn">
                        <i class="bi bi-pencil"></i> edit
                    </button>
                    <button class="btn btn-sm btn-outline-danger delete-event-btn">
                        <i class="bi bi-trash"></i> delete
                    </button>
                </div>
            </div>
        `).join('') || `<div class="alert alert-info mb-0">No events scheduled</div>`;
    }

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

    function handleDeleteEvent(eventId) {
        if (confirm('Are you sure to delete this event?')) {
            fetch(`/api/events/${eventId}`, { 
                method: 'DELETE',
                headers: { 'X-CSRFToken': '{{ csrf_token() }}' }
            }).then(response => response.ok && loadEventsForDate(getSelectedDate()));
        }
    }

    window.loadEventsForDate = function (date) {
        fetch(`/api/events/${date}`)
            .then(response => response.json())
            .then(renderEventList)
            .catch(console.error);
    };


    document.addEventListener('click', function (e) {
        const eventCard = e.target.closest('[data-event-id]');
        if (!eventCard) return;

        if (e.target.closest('.edit-btn')) {
            handleEditEvent(eventCard.dataset.eventId);
        } else if (e.target.closest('.delete-btn')) {
            handleDeleteEvent(eventCard.dataset.eventId);
        }
    });

    
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
            }
        })
    });

    

    

    
    renderCalendar(currentDate);
    
});

