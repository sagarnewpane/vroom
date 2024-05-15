// JavaScript function to toggle filter menu
function toggleFilterMenu() {
  var menu = document.getElementById("filter-menu");
  if (menu.style.display === "" || menu.style.display === "none") {
    menu.style.display = "block";
    document.querySelector(".car-container").style.flexGrow = "0.8";
  } else {
    menu.style.display = "none";
    document.querySelector(".car-container").style.flexGrow = "1";
  }
}

// // Set the initial display property of the filter menu
// window.onload = function () {
//   var menu = document.getElementById("filter-menu");
//   menu.style.display = "none";
// };
