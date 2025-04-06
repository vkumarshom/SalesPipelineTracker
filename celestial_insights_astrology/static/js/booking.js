/**
 * Booking Calendar JavaScript for Celestial Insights Astrology
 * Handles the multi-step booking form and time slot selection
 */

document.addEventListener('DOMContentLoaded', function() {
  // Elements
  const bookingForm = document.getElementById('bookingForm');
  if (!bookingForm) return; // Exit if not on booking page
  
  const step1 = document.getElementById('step1');
  const step2 = document.getElementById('step2');
  const step3 = document.getElementById('step3');
  
  const nextToStep2Button = document.getElementById('nextToStep2');
  const nextToStep3Button = document.getElementById('nextToStep3');
  const backToStep1Button = document.getElementById('backToStep1');
  const backToStep2Button = document.getElementById('backToStep2');
  const confirmBookingButton = document.getElementById('confirmBooking');
  
  const serviceIdSelect = document.getElementById('service_id');
  const datePicker = document.getElementById('datePicker');
  const timeSlotsContainer = document.getElementById('timeSlots');
  const timeInput = document.getElementById('booking_time');
  const termsCheck = document.getElementById('termsCheck');
  
  // Progress indicators
  const stepCircles = document.querySelectorAll('.step-circle');
  const progressBar = document.querySelector('.progress-bar');
  
  // Service details
  const serviceDetails = document.getElementById('serviceDetails');
  const serviceName = document.getElementById('serviceName');
  const serviceDuration = document.getElementById('serviceDuration');
  const servicePrice = document.getElementById('servicePrice');
  const serviceDescription = document.getElementById('serviceDescription');
  
  // Summary fields
  const summaryService = document.getElementById('summaryService');
  const summaryDate = document.getElementById('summaryDate');
  const summaryTime = document.getElementById('summaryTime');
  const summaryPrice = document.getElementById('summaryPrice');
  
  // Service data storage
  let services = [];
  
  // Initialize date picker
  if (datePicker) {
    flatpickr(datePicker, {
      minDate: "today",
      dateFormat: "Y-m-d",
      disable: [
        function(date) {
          // Disable past dates and weekends if needed
          return (date.getDay() === 0); // Disable Sundays
        }
      ],
      onChange: function(selectedDates, dateStr) {
        fetchAvailableTimeSlots(dateStr);
      }
    });
  }
  
  // Load service details on service selection
  if (serviceIdSelect) {
    // Get all services data
    const options = Array.from(serviceIdSelect.options);
    services = options.map(option => {
      if (option.value) {
        const parts = option.text.split(' - ');
        return {
          id: parseInt(option.value),
          name: parts[0],
          price: parts[1],
          duration: parseInt(parts[2])
        };
      }
      return null;
    }).filter(service => service !== null);
    
    // Handle service selection
    serviceIdSelect.addEventListener('change', function() {
      const selectedService = getSelectedService();
      
      if (selectedService) {
        // Display service details
        serviceDetails.classList.remove('d-none');
        serviceName.textContent = selectedService.name;
        serviceDuration.textContent = `${selectedService.duration} min`;
        servicePrice.textContent = selectedService.price;
        
        // In a real app, you might fetch the service description from the server
        serviceDescription.textContent = `This is a ${selectedService.duration}-minute consultation focused on ${selectedService.name.toLowerCase()}.`;
      } else {
        serviceDetails.classList.add('d-none');
      }
    });
    
    // Check for URL parameters to pre-select service
    const urlParams = new URLSearchParams(window.location.search);
    const serviceParam = urlParams.get('service');
    
    if (serviceParam) {
      serviceIdSelect.value = serviceParam;
      // Trigger change event to update display
      const event = new Event('change');
      serviceIdSelect.dispatchEvent(event);
    }
  }
  
  // Fetch available time slots from the server
  function fetchAvailableTimeSlots(date) {
    const selectedService = getSelectedService();
    
    if (!selectedService) {
      timeSlotsContainer.innerHTML = '<p class="text-danger">Please select a service first</p>';
      return;
    }
    
    timeSlotsContainer.innerHTML = '<p class="text-muted">Loading available times...</p>';
    
    // Get service ID
    const serviceId = serviceIdSelect.value;
    
    // Make AJAX request to get available slots
    fetch(`/booking/get_slots?service_id=${serviceId}&date=${date}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          timeSlotsContainer.innerHTML = `<p class="text-danger">${data.error}</p>`;
          return;
        }
        
        if (data.slots && data.slots.length > 0) {
          displayTimeSlots(data.slots);
        } else {
          timeSlotsContainer.innerHTML = '<p class="text-danger">No available slots for this date. Please select another date.</p>';
        }
      })
      .catch(error => {
        console.error('Error fetching time slots:', error);
        timeSlotsContainer.innerHTML = '<p class="text-danger">Error loading time slots. Please try again.</p>';
      });
  }
  
  // Display time slots
  function displayTimeSlots(slots) {
    timeSlotsContainer.innerHTML = '';
    
    const timeSlotsList = document.createElement('div');
    timeSlotsList.className = 'time-slots-container';
    
    slots.forEach(slot => {
      const timeSlot = document.createElement('div');
      timeSlot.className = 'time-slot';
      timeSlot.textContent = formatTime(slot);
      timeSlot.dataset.value = slot;
      
      timeSlot.addEventListener('click', function() {
        // Deselect all slots
        document.querySelectorAll('.time-slot').forEach(el => {
          el.classList.remove('selected');
        });
        
        // Select this slot
        this.classList.add('selected');
        
        // Update hidden input
        timeInput.value = this.dataset.value;
      });
      
      timeSlotsList.appendChild(timeSlot);
    });
    
    timeSlotsContainer.appendChild(timeSlotsList);
  }
  
  // Format time from 24h to 12h format
  function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const formattedHour = hour % 12 || 12; // Convert 0 to 12 for 12 AM
    
    return `${formattedHour}:${minutes} ${ampm}`;
  }
  
  // Format date for display
  function formatDate(dateString) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  }
  
  // Get the selected service details
  function getSelectedService() {
    const serviceId = parseInt(serviceIdSelect.value);
    return services.find(service => service.id === serviceId);
  }
  
  // Navigation between steps
  if (nextToStep2Button) {
    nextToStep2Button.addEventListener('click', function() {
      // Validate service selection
      if (!serviceIdSelect.value) {
        alert('Please select a service to continue.');
        return;
      }
      
      // Update progress indicators
      updateProgress(2);
      
      // Hide step 1, show step 2
      step1.classList.add('d-none');
      step2.classList.remove('d-none');
    });
  }
  
  if (backToStep1Button) {
    backToStep1Button.addEventListener('click', function() {
      // Update progress indicators
      updateProgress(1);
      
      // Hide step 2, show step 1
      step2.classList.add('d-none');
      step1.classList.remove('d-none');
    });
  }
  
  if (nextToStep3Button) {
    nextToStep3Button.addEventListener('click', function() {
      // Validate date and time selection
      if (!datePicker.value) {
        alert('Please select a date to continue.');
        return;
      }
      
      if (!timeInput.value) {
        alert('Please select a time slot to continue.');
        return;
      }
      
      // Update progress indicators
      updateProgress(3);
      
      // Hide step 2, show step 3
      step2.classList.add('d-none');
      step3.classList.remove('d-none');
      
      // Update booking summary
      const selectedService = getSelectedService();
      summaryService.textContent = selectedService.name;
      summaryDate.textContent = formatDate(datePicker.value);
      summaryTime.textContent = formatTime(timeInput.value);
      summaryPrice.textContent = selectedService.price;
    });
  }
  
  if (backToStep2Button) {
    backToStep2Button.addEventListener('click', function() {
      // Update progress indicators
      updateProgress(2);
      
      // Hide step 3, show step 2
      step3.classList.add('d-none');
      step2.classList.remove('d-none');
    });
  }
  
  if (termsCheck) {
    termsCheck.addEventListener('change', function() {
      confirmBookingButton.disabled = !this.checked;
    });
  }
  
  // Update progress indicators
  function updateProgress(step) {
    // Update circles
    stepCircles.forEach((circle, index) => {
      if (index < step) {
        circle.classList.add('active');
      } else {
        circle.classList.remove('active');
      }
    });
    
    // Update progress bar
    const progressPercentage = ((step - 1) / 2) * 100;
    progressBar.style.width = `${progressPercentage}%`;
    progressBar.setAttribute('aria-valuenow', progressPercentage);
  }
});
