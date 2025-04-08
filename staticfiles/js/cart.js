/**
 * Shopping Cart JavaScript for Celestial Insights Astrology
 * Handles cart item quantity updates and UX improvements
 */

document.addEventListener('DOMContentLoaded', function() {
  // Make sure we're on the cart page
  const cartPage = document.querySelector('.table.align-middle');
  if (!cartPage) return;
  
  // Quantity adjustment buttons
  const decreaseButtons = document.querySelectorAll('.decrease-quantity');
  const increaseButtons = document.querySelectorAll('.increase-quantity');
  const quantityInputs = document.querySelectorAll('.quantity-input');
  const updateButtons = document.querySelectorAll('.update-quantity-btn');
  
  // Add event listeners to decrease buttons
  decreaseButtons.forEach(button => {
    button.addEventListener('click', function() {
      const input = this.parentElement.querySelector('.quantity-input');
      const currentValue = parseInt(input.value);
      
      if (currentValue > 1) {
        input.value = currentValue - 1;
        // Show the update button
        const updateButton = this.parentElement.parentElement.querySelector('.update-quantity-btn');
        updateButton.classList.add('btn-primary');
        updateButton.classList.remove('btn-outline-primary');
      }
    });
  });
  
  // Add event listeners to increase buttons
  increaseButtons.forEach(button => {
    button.addEventListener('click', function() {
      const input = this.parentElement.querySelector('.quantity-input');
      const currentValue = parseInt(input.value);
      
      if (currentValue < 10) { // Assuming max quantity is 10
        input.value = currentValue + 1;
        // Show the update button
        const updateButton = this.parentElement.parentElement.querySelector('.update-quantity-btn');
        updateButton.classList.add('btn-primary');
        updateButton.classList.remove('btn-outline-primary');
      }
    });
  });
  
  // Add event listeners to quantity inputs for manual changes
  quantityInputs.forEach(input => {
    input.addEventListener('change', function() {
      const value = parseInt(this.value);
      
      // Enforce min/max values
      if (value < 1) {
        this.value = 1;
      } else if (value > 10) {
        this.value = 10;
      }
      
      // Show the update button
      const updateButton = this.parentElement.parentElement.querySelector('.update-quantity-btn');
      updateButton.classList.add('btn-primary');
      updateButton.classList.remove('btn-outline-primary');
    });
  });
  
  // Add confirmation for remove buttons
  const removeButtons = document.querySelectorAll('button[type="submit"].btn-outline-danger');
  
  removeButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      if (!confirm('Are you sure you want to remove this item from your cart?')) {
        e.preventDefault();
      }
    });
  });
  
  // Calculate totals on quantity change (client-side preview)
  function recalculateItemTotal(quantityInput) {
    const row = quantityInput.closest('tr');
    const priceCell = row.querySelector('td:nth-child(2)');
    const totalCell = row.querySelector('td:nth-child(4)');
    
    if (priceCell && totalCell) {
      const priceText = priceCell.textContent;
      const price = parseFloat(priceText.replace('$', ''));
      const quantity = parseInt(quantityInput.value);
      
      if (!isNaN(price) && !isNaN(quantity)) {
        const total = (price * quantity).toFixed(2);
        totalCell.textContent = `$${total}`;
      }
    }
  }
  
  // Update item totals when quantity changes
  quantityInputs.forEach(input => {
    input.addEventListener('change', function() {
      recalculateItemTotal(this);
    });
  });
  
  // Also update when increase/decrease buttons are clicked
  decreaseButtons.forEach(button => {
    button.addEventListener('click', function() {
      const input = this.parentElement.querySelector('.quantity-input');
      recalculateItemTotal(input);
    });
  });
  
  increaseButtons.forEach(button => {
    button.addEventListener('click', function() {
      const input = this.parentElement.querySelector('.quantity-input');
      recalculateItemTotal(input);
    });
  });
  
  // Disable form submission on Enter key to prevent accidental updates
  const cartForms = document.querySelectorAll('.cart-quantity-form');
  
  cartForms.forEach(form => {
    form.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const updateButton = this.querySelector('.update-quantity-btn');
        updateButton.click();
      }
    });
  });
  
  // Proceed to checkout button - check if cart has items
  const checkoutButton = document.querySelector('a[href="/checkout"]');
  
  if (checkoutButton) {
    const cartItems = document.querySelectorAll('tbody tr');
    
    if (cartItems.length === 0) {
      checkoutButton.classList.add('disabled');
      checkoutButton.setAttribute('aria-disabled', 'true');
      checkoutButton.addEventListener('click', function(e) {
        e.preventDefault();
        alert('Your cart is empty. Please add items to your cart before checkout.');
      });
    }
  }
});
