document.addEventListener('DOMContentLoaded', function () {
  // Only executed on the visualization. html page
  const friendSelector = document.getElementById('friend-selector');
  const daysContainer = document.getElementById('days');
  const monthYear = document.getElementById('month-year');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');

  if (!friendSelector || !daysContainer || !monthYear || !prevBtn || !nextBtn) {
    // Not a visualization page, return directly
    return;
  }

  let currentMonthDate = new Date();

  function renderEventList(events) {
    const container = document.getElementById('friend-today-events');
    if (!events || events.length === 0) {
      container.innerHTML = `<div class="alert alert-info mb-0">
        <i class="bi bi-info-circle me-2"></i>No events scheduled for this day
      </div>`;
      return;
    }
    container.innerHTML = events.map(event => `
      <div class="event-card mb-3 p-2 border rounded">
        <div class="d-flex justify-content-between">
          <strong class="event-title">${event.title}</strong>
          <small class="text-muted">
            ${event.start_time} - ${event.end_time}
          </small>
        </div>
        ${event.description ? `<p class="mt-1 mb-0 small event-description">${event.description}</p>` : ''}
      </div>
    `).join('');
  }

  function fetchFriendDayEvents(friendId, dateStr) {
    fetch(`/api/friend_calendar/${friendId}?date=${dateStr}`)
      .then(res => res.json())
      .then(data => {
        renderEventList(data.events || []);
        const displayDate = new Date(dateStr);
        const options = { weekday: 'long', month: 'long', day: 'numeric' };
        document.getElementById('friend-display-date').textContent = displayDate.toLocaleDateString('en-US', options);
      })
      .catch(err => {
        renderEventList([]);
        console.error('Error loading friend day events:', err);
      });
  }

  function renderCalendar(eventDurations) {
    daysContainer.innerHTML = '';

    const year = currentMonthDate.getFullYear();
    const month = currentMonthDate.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const lastDay = new Date(year, month + 1, 0).getDate();

    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    monthYear.textContent = `${months[month]} ${year}`;

    const totalCells = firstDay + lastDay;
    const rows = Math.ceil(totalCells / 7);

    let date = 1;
    for (let r = 0; r < rows; r++) {
      const row = document.createElement('div');
      row.className = 'row g-0';
      for (let c = 0; c < 7; c++) {
        const cellIndex = r * 7 + c;
        const dayCell = document.createElement('div');
        dayCell.className = 'col p-2 text-center border';

        if (cellIndex >= firstDay && date <= lastDay) {
          const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
          const duration = eventDurations[dateStr] || 0;

          dayCell.textContent = date;
          if (duration === 0) {
            dayCell.style.backgroundColor = 'white';
          } else if (duration <= 2) {
            dayCell.style.backgroundColor = '#00ff00';
          } else if (duration <= 4) {
            dayCell.style.backgroundColor = '#61f100';
          } else if (duration <= 6) {
            dayCell.style.backgroundColor = '#89e200';
          } else if (duration <= 8) {
            dayCell.style.backgroundColor = '#a3d200';
          } else if (duration <= 10) {
            dayCell.style.backgroundColor = '#b6c300';
          } else if (duration <= 12) {
            dayCell.style.backgroundColor = '#c7b200';
          } else if (duration <= 14) {
            dayCell.style.backgroundColor = '#d5a100';
          } else if (duration <= 16) {
            dayCell.style.backgroundColor = '#e28d00';
          } else if (duration <= 18) {
            dayCell.style.backgroundColor = '#ee7700';
          } else if (duration <= 20) {
            dayCell.style.backgroundColor = '#f75e00';
          } else if (duration <= 22) {
            dayCell.style.backgroundColor = '#fd3f00';
          } else if (duration <= 24) {
            dayCell.style.backgroundColor = '#ff0000';
          } else {
            dayCell.style.backgroundColor = '#cc0000';
            dayCell.style.color = 'white';
          }

          dayCell.style.cursor = 'pointer';
          dayCell.addEventListener('click', function () {
            const friendId = friendSelector.value;
            if (friendId) fetchFriendDayEvents(friendId, dateStr);
          });

          date++;
        }

        row.appendChild(dayCell);
      }
      daysContainer.appendChild(row);
    }
  }

  prevBtn.addEventListener('click', () => {
    currentMonthDate.setMonth(currentMonthDate.getMonth() - 1);
    const friendId = friendSelector.value;
    if (friendId) fetchFriendCalendar(friendId);
  });

  nextBtn.addEventListener('click', () => {
    currentMonthDate.setMonth(currentMonthDate.getMonth() + 1);
    const friendId = friendSelector.value;
    if (friendId) fetchFriendCalendar(friendId);
  });

  function fetchFriendCalendar(friendId) {
    fetch(`/api/friend_calendar/${friendId}`)
      .then(res => res.json())
      .then(data => renderCalendar(data.eventDurations || {}))
      .catch(err => console.error('Error loading friend calendar:', err));
  }

  friendSelector.addEventListener('change', function () {
    const friendId = this.value;
    if (friendId) fetchFriendCalendar(friendId);
  });
});