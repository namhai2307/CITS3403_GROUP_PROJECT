document.addEventListener('DOMContentLoaded', function () {
  const links = document.querySelectorAll('.help-sidebar a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      links.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
});