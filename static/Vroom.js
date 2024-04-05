document.getElementById('carForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var location = document.getElementById('id_location').value;
    var pickup_datetime = document.getElementById('id_pickup_datetime').value;
    var dropoff_datetime = document.getElementById('id_dropoff_datetime').value;

    localStorage.setItem('location', location);
    localStorage.setItem('pickup_datetime', pickup_datetime);
    localStorage.setItem('dropoff_datetime', dropoff_datetime);

    this.submit();
});