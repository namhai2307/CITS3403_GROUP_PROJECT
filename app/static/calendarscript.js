function showForm(formID) {
    document.querySelectorAll(".form-box").forEach(form => form.classList.remove("active"));
    document.getElementById(formID).classList.add("active")
}

document.addEventListener('DOMContentLoaded', function() {
    const monthYear = document.getElementById("month-year");
    const daysContainer = document.getElementById("days");
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

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
            dayDiv.addEventListener('click', function() {
                const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                window.location.href = `/dashboard?date=${dateStr}`;
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

    // Previous button event listener - toggle previous month
    prevButton.addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    // Next button event listener - toggle next month
    nextButton.addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    // Initial render
    renderCalendar(currentDate);

});
