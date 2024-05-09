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

document.addEventListener('DOMContentLoaded', function() {
    fetch('/path/to/your/purchase/history/api')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('historyTable').getElementsByTagName('tbody')[0];
        data.forEach(purchase => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${purchase.date}</td>
                <td>${purchase.product_name}</td>
                <td>${purchase.quantity}</td>
                <td>$${purchase.price}</td>
                <td>${purchase.status}</td>
                <td>
                    <button onclick="reorder(${purchase.product_id}, ${purchase.quantity})" class="btn btn-primary">Reorder</button>
                </td>
            `;
        });
    })
    .catch(error => console.error('Error loading purchase history:', error));
});

function reorder(productId, quantity) {
    console.log('Reordering product ID:', productId, 'Quantity:', quantity);
    // Add your code here to handle the reorder action, such as sending a POST request to your server
}

const productsDiv = document.getElementById('products');
let newContent = '';
response.forEach(function(product) {
    newContent += `<p>${product.name} - ${product.category}: $${product.price}</p>`;
});
productsDiv.innerHTML = newContent;