document.addEventListener('DOMContentLoaded', function () {
    // Attach a submit event listener to the registration form
    document.querySelector('form').onsubmit = function() {
        // Get values from the password and confirm password fields
        var password = document.getElementById('password').value;
        var confirmPassword = document.getElementById('confirm-password').value;

        // Check if passwords match
        if (password !== confirmPassword) {
            // If passwords do not match, show an alert
            alert('Passwords do not match.');
            // Prevent form submission
            return false;
        }
        // If passwords match, allow form submission
        return true;
    };
});