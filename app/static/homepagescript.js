// homepagescript.js 

document.addEventListener("DOMContentLoaded", function () {
  // Hide all info sections initially on the global webpage
  document.querySelectorAll('.info-section').forEach(el => {
    el.style.display = "none";
  });

  window.showInfo = function (infoID) {
    // Hide all info sections (when it's loaded hide all info again)
    document.querySelectorAll('.info-section').forEach(el => {
      el.style.display = "none";
    });

    // Display the info when button is clicked
    const target = document.getElementById(infoID);
    if (target) {
      target.style.display = "block";
    }
  };
});
