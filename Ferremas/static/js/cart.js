document.addEventListener('DOMContentLoaded', (event) => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productoId = this.getAttribute('data-producto-id');
            fetch(`/carro/add/${productoId}/`, {
                method: 'GET',
            }).then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        const cartCount = document.getElementById('cart-count');
                        cartCount.innerText = data.cart_count;
                    });
                } else {
                    console.error('Error al añadir al carrito');
                }
            }).catch(error => console.error('Error:', error));
        });
    });
});
