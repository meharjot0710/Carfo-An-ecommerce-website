function addToCart(productData) {
    // Get cart items from localStorage or initialize an empty array
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Check if the product is already in the cart
    const existingItem = cart.find(item => item.productId === productData.productId);
    if (existingItem) {
        // If the product is already in the cart, increase its quantity
        existingItem.quantity += 1;
    } else {
        // If the product is not in the cart, add it to the cart
        cart.push({ 
            productId: productData.productId,
            quantity: 1,
            image: productData.image,
            name: productData.name,
            price: productData.price
        });
        
    }
    
    // Save the updated cart back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Update the cart display
    updateCartDisplay();
    alert('Your order has been placed.');
}

function updateCartDisplay() {
    // Get cart items from localStorage or initialize an empty array
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Get the element where cart items will be displayed
    let cartItemsElement = document.getElementById('cart-items');

    // Clear the cart items element before updating
    cartItemsElement.innerHTML = '';

    // Loop through each item in the cart and create HTML elements to display them
    cart.forEach(item => {
        let itemElement = document.createElement('div');
        itemElement.classList.add('cart-item');
        itemElement.innerHTML = `
        <img src="${item.image}" alt="${item.name}">
        <div class="item-details">
            <p>${item.name} - Quantity: ${item.quantity} - Price: ${item.price}</p>
        </div>`;
        cartItemsElement.appendChild(itemElement);
        alert('Your order has been placed.');
    });
}
