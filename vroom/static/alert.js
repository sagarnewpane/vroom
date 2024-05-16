// Alert
document.getElementById("carForm").addEventListener("submit", function (event) {
  var pickup_datetime = new Date(
    document.getElementById("id_pickup_datetime").value
  );
  var dropoff_datetime = new Date(
    document.getElementById("id_dropoff_datetime").value
  );
  var duration = (dropoff_datetime - pickup_datetime) / (1000 * 60 * 60); // convert milliseconds to hours

  var current_datetime = new Date(); // get current date and time

  var errorMessage = "";
  if (pickup_datetime < current_datetime) {
    errorMessage = "Pickup date cannot be in the past.";
  } else if (dropoff_datetime <= pickup_datetime) {
    errorMessage = "Dropoff time must be greater than pickup time.";
  } else if (duration < 5) {
    errorMessage = "Minimum booking duration is 5 hours.";
  }

  if (errorMessage) {
    document.querySelector(".errorMessage").textContent = errorMessage; // Update the error message in the vertical container
    event.preventDefault(); // prevent form from submitting
  } else {
    // Form submission is valid
    this.submit();
  }
});