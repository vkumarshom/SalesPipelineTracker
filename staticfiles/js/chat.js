document.addEventListener('DOMContentLoaded', function() {
    // Chat widget elements
    const chatTrigger = document.querySelector('.chat-trigger');
    const chatWidget = document.querySelector('.chat-widget');
    const chatMinimize = document.querySelector('.chat-minimize');
    const chatClose = document.querySelector('.chat-close');
    const chatBody = document.querySelector('.chat-body');
    const chatInput = document.querySelector('.chat-input');
    const chatSend = document.querySelector('.chat-send');
    const chatDisplayName = document.querySelector('.chat-display-name');

    // WhatsApp configuration defaults (will be updated via API)
    let whatsappNumber = ""; 
    let whatsappMessage = "Hello, I'd like to book an astrology consultation.";
    let displayName = "MetaMystic Astrology";
    
    // Fetch WhatsApp configuration from API
    fetch('/api/whatsapp-config/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                whatsappNumber = data.phone_number.replace(/\s+/g, '').replace(/[+]/g, '');
                whatsappMessage = data.default_message;
                displayName = data.display_name;
                
                // Update the display name in the chat header if the element exists
                if (chatDisplayName) {
                    chatDisplayName.textContent = displayName;
                }
            } else {
                console.log('Using default WhatsApp configuration');
            }
        })
        .catch(error => {
            console.error('Error fetching WhatsApp configuration:', error);
        });
    
    // Chat options and responses
    const chatOptions = [
        { id: 'services', text: 'What services do you offer?' },
        { id: 'pricing', text: 'How much do consultations cost?' },
        { id: 'booking', text: 'How can I book a session?' },
        { id: 'contact', text: 'I want to speak to an astrologer' }
    ];
    
    const chatResponses = {
        'services': `<p>At MetaMystic, we offer a range of astrology services including:</p>
                    <ul>
                        <li>Birth Chart Analysis</li>
                        <li>Compatibility Readings</li>
                        <li>Transit Forecasts</li>
                        <li>Solar Return Charts</li>
                        <li>Career & Life Path Guidance</li>
                    </ul>
                    <p>Would you like to know more about any specific service?</p>`,
        'pricing': `<p>Our consultation services are priced as follows:</p>
                    <ul>
                        <li>30-minute session: £50</li>
                        <li>60-minute session: £90</li>
                        <li>90-minute session: £130</li>
                        <li>Written reports starting at £75</li>
                    </ul>
                    <p>We also offer package discounts for multiple sessions.</p>`,
        'booking': `<p>Booking a session is easy!</p>
                    <p>You can book directly through our website's calendar system, where you'll see all available time slots. Simply select a service, choose a date and time, and complete your booking.</p>
                    <p>Would you like me to help you book a session now?</p>`,
        'contact': `<p>I'd be happy to connect you with one of our astrologers for a personal consultation.</p>`
    };

    // Toggle chat visibility
    if (chatTrigger) {
        chatTrigger.addEventListener('click', function() {
            chatWidget.classList.remove('hidden');
            chatTrigger.classList.add('hidden');
            // Show welcome message and options
            showWelcomeMessage();
        });
    }

    // Minimize chat
    if (chatMinimize) {
        chatMinimize.addEventListener('click', function() {
            chatWidget.classList.toggle('minimized');
        });
    }

    // Close chat
    if (chatClose) {
        chatClose.addEventListener('click', function() {
            chatWidget.classList.add('hidden');
            chatTrigger.classList.remove('hidden');
        });
    }

    // Send message on button click
    if (chatSend) {
        chatSend.addEventListener('click', sendMessage);
    }

    // Send message on Enter key
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Show welcome message and options
    function showWelcomeMessage() {
        // Clear chat
        chatBody.innerHTML = '';
        
        // Add welcome message
        addMessage(`Hello! 👋 Welcome to ${displayName}. How can I help you today?`, 'bot');
        
        // Show typing indicator
        showTypingIndicator();
        
        // Add options after a short delay
        setTimeout(() => {
            removeTypingIndicator();
            addOptions();
        }, 1000);
    }

    // Add a message to the chat
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.innerHTML = message;
        chatBody.appendChild(messageElement);
        
        // Scroll to bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Add chat options
    function addOptions() {
        const optionsContainer = document.createElement('div');
        optionsContainer.classList.add('options-container');
        
        chatOptions.forEach(option => {
            const optionButton = document.createElement('button');
            optionButton.classList.add('chat-option');
            optionButton.textContent = option.text;
            optionButton.dataset.optionId = option.id;
            
            optionButton.addEventListener('click', function() {
                // Add user message
                addMessage(option.text, 'user');
                
                // Clear options
                optionsContainer.remove();
                
                // Show typing indicator
                showTypingIndicator();
                
                // Process the option after a short delay
                setTimeout(() => {
                    removeTypingIndicator();
                    processOption(option.id);
                }, 1500);
            });
            
            optionsContainer.appendChild(optionButton);
        });
        
        chatBody.appendChild(optionsContainer);
        
        // Scroll to bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Process chat option
    function processOption(optionId) {
        // Get response for the selected option
        const response = chatResponses[optionId] || "I'm sorry, I don't have information on that topic yet.";
        
        // Add bot message
        addMessage(response, 'bot');
        
        // If the option is 'contact', add WhatsApp button
        if (optionId === 'contact') {
            addWhatsAppButton();
        } else {
            // Show typing indicator
            setTimeout(() => {
                showTypingIndicator();
                
                // Add "anything else" message after a delay
                setTimeout(() => {
                    removeTypingIndicator();
                    addMessage("Is there anything else you'd like to know?", 'bot');
                    addOptions();
                }, 1500);
            }, 1000);
        }
    }

    // Add WhatsApp button
    function addWhatsAppButton() {
        const buttonContainer = document.createElement('div');
        buttonContainer.classList.add('button-container');
        
        const whatsappButton = document.createElement('a');
        whatsappButton.classList.add('whatsapp-button');
        whatsappButton.href = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;
        whatsappButton.target = '_blank';
        whatsappButton.innerHTML = '<i class="fab fa-whatsapp"></i> Connect on WhatsApp';
        
        buttonContainer.appendChild(whatsappButton);
        chatBody.appendChild(buttonContainer);
        
        // Scroll to bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Send message function
    function sendMessage() {
        const message = chatInput.value.trim();
        
        if (message) {
            // Add user message
            addMessage(message, 'user');
            
            // Clear input
            chatInput.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Process message after a short delay
            setTimeout(() => {
                removeTypingIndicator();
                processMessage(message);
            }, 1500);
        }
    }

    // Process user message
    function processMessage(message) {
        // Simple keyword matching
        const messageLower = message.toLowerCase();
        
        if (messageLower.includes('service') || messageLower.includes('offer')) {
            processOption('services');
        } else if (messageLower.includes('price') || messageLower.includes('cost') || messageLower.includes('fee')) {
            processOption('pricing');
        } else if (messageLower.includes('book') || messageLower.includes('appointment') || messageLower.includes('schedule')) {
            processOption('booking');
        } else if (messageLower.includes('speak') || messageLower.includes('talk') || messageLower.includes('chat') || messageLower.includes('person')) {
            processOption('contact');
        } else {
            // Default response
            addMessage("I'm not sure I understand. Please select one of these options:", 'bot');
            addOptions();
        }
    }

    // Show typing indicator
    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        chatBody.appendChild(typingIndicator);
        
        // Scroll to bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
});
