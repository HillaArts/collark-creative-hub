// app.js located in /static/js/

document.addEventListener('DOMContentLoaded', function() {
    var alertLinks = document.querySelectorAll('.alert-link');
    
    alertLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            alert('You clicked a link!');
        });
    });
});