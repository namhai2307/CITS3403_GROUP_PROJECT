document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('toggle-dark');
  
  if (localStorage.getItem('dark-mode') === 'on') {
    document.body.classList.add('dark-mode');
  }
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      document.body.classList.toggle('dark-mode');
      
      if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('dark-mode', 'on');
      } else {
        localStorage.setItem('dark-mode', 'off');
      }
    });
  }
});