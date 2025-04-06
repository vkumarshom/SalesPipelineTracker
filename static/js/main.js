/**
 * Main JavaScript for Celestial Insights Astrology
 * Contains general site functionality
 */

document.addEventListener('DOMContentLoaded', function() {
  
  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Initialize popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      if (this.getAttribute('href') !== "#") {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 70, // Offset for fixed header
            behavior: 'smooth'
          });
        }
      }
    });
  });
  
  // Add active class to current nav item based on URL
  const currentLocation = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
  navLinks.forEach(link => {
    const linkPath = link.getAttribute('href');
    
    if (linkPath === currentLocation || 
        (linkPath !== '/' && currentLocation.includes(linkPath))) {
      link.classList.add('active');
    }
  });
  
  // Newsletter form submission (placeholder)
  const newsletterForms = document.querySelectorAll('form:not([action])');
  
  newsletterForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Get the email input
      const emailInput = form.querySelector('input[type="email"]');
      
      if (emailInput && emailInput.value) {
        // Show success message
        const formParent = form.parentElement;
        const successMessage = document.createElement('div');
        successMessage.className = 'alert alert-success mt-3';
        successMessage.textContent = 'Thank you for subscribing to our newsletter!';
        
        // Replace form with success message
        form.style.display = 'none';
        formParent.appendChild(successMessage);
        
        // Clear the form
        form.reset();
        
        // In a real application, you would send the data to the server here
      }
    });
  });
  
  // Function to check if element is in viewport
  function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }
  
  // Add fade-in animation to elements when they come into view
  function handleScrollAnimations() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    animateElements.forEach(element => {
      if (isInViewport(element)) {
        element.classList.add('fade-in');
      }
    });
  }
  
  // Add animate-on-scroll class to common elements
  const animatableElements = document.querySelectorAll('.feature-icon, .service-icon, .card, .hero-image');
  animatableElements.forEach(element => {
    element.classList.add('animate-on-scroll');
  });
  
  // Listen for scroll events to trigger animations
  window.addEventListener('scroll', handleScrollAnimations);
  
  // Trigger on initial load
  handleScrollAnimations();
  
  // Back to top button functionality
  const backToTopButton = document.getElementById('back-to-top');
  
  if (backToTopButton) {
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'block';
      } else {
        backToTopButton.style.display = 'none';
      }
    });
    
    backToTopButton.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
});
