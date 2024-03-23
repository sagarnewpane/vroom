  document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
  
    loginForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      // Here you can add your login logic
      console.log('Username:', username);
      console.log('Password:', password);
      // Redirect to dashboard or perform other actions after successful login
    });
  
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const username = document.getElementById('username').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      // Here you can add your signup logic
      console.log('Username:', username);
      console.log('Email:', email);
      console.log('Password:', password);
      // Redirect to login page or perform other actions after successful signup
    });
  });
  