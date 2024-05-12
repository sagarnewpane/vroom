document.addEventListener('DOMContentLoaded', function() {
  var dropdownButton = document.getElementById('dropdownButton');
  var dropdownContent = document.getElementById('dropdownContent');

  dropdownButton.addEventListener('click', function(event) {
      if (dropdownContent.style.display === 'none' || dropdownContent.style.display === '') {
          dropdownContent.style.display = 'block';
      } else {
          dropdownContent.style.display = 'none';
      }
      event.stopPropagation(); // Stop the event from propagating to the window
  });

  // Close the dropdown if the user clicks outside of it
  window.addEventListener('click', function(event) {
      if (!dropdownButton.contains(event.target) && !dropdownContent.contains(event.target)) {
          dropdownContent.style.display = 'none';
      }
  });
});


window.addEventListener('load', function() {
  var navbarLinks = document.getElementById('navbarLinks');

  if (window.innerWidth <= 768) {
    navbarLinks.style.display = 'none';
  }
});

document.getElementById('navbarToggler').addEventListener('click', function() {
  var navbarLinks = document.getElementById('navbarLinks');

  if (navbarLinks.style.display === 'none') {
    navbarLinks.style.display = 'flex';
  } else {
    navbarLinks.style.display = 'none';
  }
});

window.addEventListener('resize', function() {
  var navbarLinks = document.getElementById('navbarLinks');

  if (window.innerWidth > 768) {
    navbarLinks.style.display = 'flex';
  } else {
    navbarLinks.style.display = 'none';
  }
});