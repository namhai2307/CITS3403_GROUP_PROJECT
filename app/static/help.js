/**
 * @fileoverview Help sidebar navigation functionality.
 *
 * This script manages the behavior of the help sidebar links. It ensures that the active link is visually highlighted when clicked, providing a clear indication of the currently selected section.
 *
 * Features:
 * - Dynamically highlights the active link in the help sidebar
 * - Removes the `active` class from previously selected links
 * - Adds the `active` class to the clicked link
 *
 * Dependencies:
 * - DOM elements with the class: `help-sidebar`
 * - Anchor (`<a>`) elements with `href` attributes starting with `#`
 *
 */

document.addEventListener('DOMContentLoaded', function () {
  const links = document.querySelectorAll('.help-sidebar a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      links.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
});