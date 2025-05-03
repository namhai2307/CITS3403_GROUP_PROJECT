function showForm(formID) {
    document.querySelectorAll(".form-box").forEach(form => form.classList.remove("active"));
    document.getElementById(formID).classList.add("active")
}

document.addEventListener('DOMContentLoaded', function(){

    const monthYear = document.getElementById("month-year");
    const daysContainer = document.getElementById("days");
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

    const urlParams = new URLSearchParams(window.location.search);
    const urlDate = urlParams.get('date');
    let selectedDate = urlDate ? new Date(urlDate) : null;

    // If there is a URL date parameter, the initial display shows the month in which the date is located
    let currentDate = urlDate ? new Date(urlDate) : new Date();


    
    console.log(monthYear); //for debug
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
            dayDiv.classList.add('day-number'); // Add clickable classes

            
            // Highlight Logic
            const isSelected = selectedDate && 
                             i === selectedDate.getDate() && 
                             month === selectedDate.getMonth();
            
            

            if (isSelected) dayDiv.classList.add('selected-day');
           

            // Add click event
            dayDiv.addEventListener('click', function() {
                
                if (month !== currentDate.getMonth()) {
                    currentDate = new Date(year, month, 1);
                }
                const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(i).padStart(2,'0')}`;
                window.location.href = `/dashboard?date=${dateStr}`;
            });

            daysContainer.appendChild(dayDiv);
        }
        // next Month:
        const nextMonthStartDay = 7 - new Date(year, month + 1, 0).getDay() - 1;
        for (let i = 1; i <= nextMonthStartDay; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            dayDiv.classList.add('fade');
            daysContainer.appendChild(dayDiv);
        }

    }

    prevButton.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextButton.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    
    window.addEventListener('popstate', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const newUrlDate = urlParams.get('date');
        
        
        if ((newUrlDate && !selectedDate) || 
            (!newUrlDate && selectedDate) || 
            (newUrlDate && selectedDate && newUrlDate !== selectedDate.toISOString().split('T')[0])) {
            selectedDate = newUrlDate ? new Date(newUrlDate) : null;
            currentDate = newUrlDate ? new Date(newUrlDate) : new Date();
            renderCalendar(currentDate);
        }
    });

    
    renderCalendar(currentDate);

    });
