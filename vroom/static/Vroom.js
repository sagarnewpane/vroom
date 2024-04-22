document.getElementById('carForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var location = document.getElementById('id_location').value;
    var pickup_datetime = document.getElementById('id_pickup_datetime').value;
    var dropoff_datetime = document.getElementById('id_dropoff_datetime').value;

    localStorage.setItem('location', location);
    localStorage.setItem('pickup_datetime', pickup_datetime);
    localStorage.setItem('dropoff_datetime', dropoff_datetime);

    // Do not submit the form programmatically here
});

flatpickr(".flatpickr", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
});

// Implementing minimum booking hours to be 5 hours and allow only dropoff time to be greater than pickup time
document.getElementById('carForm').addEventListener('submit', function(event) {
    var pickup_datetime = new Date(document.getElementById('id_pickup_datetime').value);
    var dropoff_datetime = new Date(document.getElementById('id_dropoff_datetime').value);
    var duration = (dropoff_datetime - pickup_datetime) / (1000 * 60 * 60); // convert milliseconds to hours

    if (dropoff_datetime <= pickup_datetime) {
        alert('Dropoff time must be greater than pickup time.');
        event.preventDefault(); // prevent form from submitting
    } else if (duration < 5) {
        alert('Minimum booking duration is 5 hours.');
        event.preventDefault(); // prevent form from submitting
    } else {
        // Form submission is valid
        this.submit();
    }
});
