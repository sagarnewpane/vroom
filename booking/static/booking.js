window.onload = function () {
  var location = localStorage.getItem("location");
  var pickup_datetime = localStorage.getItem("pickup_datetime");
  var dropoff_datetime = localStorage.getItem("dropoff_datetime");

  if (location) {
    document.getElementById("id_location").value = location;
  }
  if (pickup_datetime) {
    document.getElementById("id_pickup_datetime").value = pickup_datetime;
  }
  if (dropoff_datetime) {
    document.getElementById("id_dropoff_datetime").value = dropoff_datetime;
  }

  var hourlyRate = parseFloat(document.getElementById("hourly-rate").value);

  var calculateTotalCost = function () {
    var pickupTime = new Date(
      document.getElementById("id_pickup_datetime").value.replace(" ", "T")
    );
    var dropoffTime = new Date(
      document.getElementById("id_dropoff_datetime").value.replace(" ", "T")
    );

    if (pickupTime && dropoffTime) {
      var diff = Math.abs(dropoffTime - pickupTime); // difference in milliseconds
      var hours = diff / 1000 / 60 / 60; // convert to hours

        // Repalce NaN with 0 in the estimated price field
      var totalCost = hours * hourlyRate;
      if (isNaN(totalCost)) {
        totalCost = 0;
      }

      document.getElementById("estimated_price").value = totalCost.toFixed(2);
    }
  };



  // Add event listeners to the pickup and dropoff datetime fields
  document
    .getElementById("id_pickup_datetime")
    .addEventListener("change", calculateTotalCost);
  document
    .getElementById("id_dropoff_datetime")
    .addEventListener("change", calculateTotalCost);

  calculateTotalCost(); // Invoke the function to calculate the total cost

  document
    .querySelector("#disagreeButton")
    .addEventListener("click", function () {
      document.querySelector("#termsModal").style.display = "none";
    });
};

flatpickr(".flatpickr", {
  enableTime: true,
  dateFormat: "Y-m-d H:i",
});

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
  // if (dropoff_datetime <= pickup_datetime) {
  //   errorMessage = "Dropoff time must be greater than pickup time.";
  // } else if (duration < 5) {
  //   errorMessage = "Minimum booking duration is 5 hours.";
  // }

  if (pickup_datetime < current_datetime) {
    errorMessage = "Pickup date cannot be in the past.";
  } else if (dropoff_datetime <= pickup_datetime) {
    errorMessage = "Dropoff time must be greater than pickup time.";
  } else if (duration < 5) {
    errorMessage = "Minimum booking duration is 5 hours.";
  }
  
  console.log(errorMessage);

  if (errorMessage) {
    document.querySelector(".errorMessage").textContent = errorMessage; // Update the error message in the vertical container
    event.preventDefault(); // prevent form from submitting
  } else {
    // Form submission is valid
    // Show the terms and conditions modal
    document.querySelector("#termsModal").style.display = "block";
    event.preventDefault(); // prevent form from submitting until terms are agreed to
  }
});

document.querySelector("#agreeButton").addEventListener("click", function () {
  document.querySelector("#termsModal").style.display = "none";
  document.querySelector("#carForm").submit(); // Manually submit the form
});

document
  .querySelector("#disagreeButton")
  .addEventListener("click", function () {
    document.querySelector("#termsModal").style.display = "none";
  });
