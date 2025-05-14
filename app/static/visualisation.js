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
        const formattedDate = displayDate.toLocaleDateString('en-US', options);
        document.getElementById('friend-schedule-header').innerHTML =
          `<i class="bi bi-list-task me-2"></i>${formattedDate} Schedule`;
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
      dayDiv.classList.add('day-cell');
      dayDiv.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;

      // Heatmap coloring
      const dateStr = dayDiv.dataset.date;
      const duration = eventDurations[dateStr] || 0;
      if (duration === 0) {
        dayDiv.style.backgroundColor = 'white';
      } else if (duration <= 2) {
        dayDiv.style.backgroundColor = '#ffcccc';
      } else if (duration <= 5) {
        dayDiv.style.backgroundColor = '#ff6666';
      } else {
        dayDiv.style.backgroundColor = '#cc0000';
        dayDiv.style.color = 'white';
      }

      // Highlight today
      const today = new Date();
      if (
        i === today.getDate() &&
        month === today.getMonth() &&
        year === today.getFullYear()
      ) {
        dayDiv.classList.add('today');
      }

      // Click event
      dayDiv.addEventListener('click', function () {
        document.querySelectorAll('.day-cell').forEach(cell => cell.classList.remove('today'));
        dayDiv.classList.add('today');
        const friendId = friendSelector.value;
        if (friendId) fetchFriendDayEvents(friendId, dayDiv.dataset.date);
      });

      daysContainer.appendChild(dayDiv);
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