// Main JavaScript for MetaMystic

document.addEventListener('DOMContentLoaded', function() {
    console.log('MetaMystic JS initialized');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add smooth scrolling for all links that point to an ID
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add animation on scroll
    function animateOnScroll() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                element.classList.add('animated');
            }
        });
    }
    
    // Run once on page load
    animateOnScroll();
    
    // Add scroll event listener
    window.addEventListener('scroll', animateOnScroll);
    
    // Handle the subscription form
    const subscriptionForm = document.querySelector('.newsletter form');
    if (subscriptionForm) {
        subscriptionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email) {
                // Here you would normally send the email to your server
                console.log('Subscription requested for:', email);
                
                // Show success message
                const button = this.querySelector('button');
                const originalText = button.textContent;
                button.textContent = 'Subscribed!';
                button.classList.add('btn-success');
                button.classList.remove('btn-outline-light');
                
                // Clear the input
                emailInput.value = '';
                
                // Reset after 3 seconds
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-light');
                }, 3000);
            }
        });
    }
    
    // Add chakra hover effects
    const chakraCards = document.querySelectorAll('.chakra-card');
    chakraCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const symbol = this.querySelector('.chakra-symbol');
            if (symbol) {
                symbol.style.transform = 'scale(1.2)';
                symbol.style.transition = 'transform 0.3s ease';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const symbol = this.querySelector('.chakra-symbol');
            if (symbol) {
                symbol.style.transform = 'scale(1)';
            }
        });
    });
});
