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
