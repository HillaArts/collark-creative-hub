function fetchProducts() {
    const category = document.getElementById('category').value;
    $.ajax({
        url: '/filtered_products',
        type: 'GET',
        data: {
            category: category
        },
        success: function(response) {
            const productsDiv = document.getElementById('products');
            productsDiv.innerHTML = '';
            response.forEach(function(product) {
                productsDiv.innerHTML += `<p>${product.name} - ${product.category}: $${product.price}</p>`;
            });
        }
    });
}
