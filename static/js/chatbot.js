/**
 * Ulimi Wise - Chatbot JavaScript
 * Handles chatbot interaction, voice input, and text-to-speech
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Chatbot script loaded');
    
    // Get DOM elements
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const voiceResponseToggle = document.getElementById('voiceResponseToggle');
    
    // Initialize chat functionality
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            sendMessage();
        });
    }
    
    // Scroll to the bottom of chat messages
    scrollToBottom();
    
    // Focus the message input field
    if (messageInput) {
        messageInput.focus();
    }
    
    // Setup voice response toggle
    if (voiceResponseToggle) {
        // Check localStorage for preference
        const voiceEnabled = localStorage.getItem('voiceResponseEnabled') === 'true';
        voiceResponseToggle.checked = voiceEnabled;
        
        voiceResponseToggle.addEventListener('change', function() {
            localStorage.setItem('voiceResponseEnabled', this.checked);
        });
    }
});

/**
 * Send message to the chatbot
 */
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    
    // Clear input field
    messageInput.value = '';
    
    // Show typing indicator
    addTypingIndicator();
    
    // Send message to server
    const formData = new FormData();
    formData.append('message', message);
    
    fetch('/chatbot/message', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response to chat
        addMessageToChat('bot', data.response);
        
        // Play voice response if enabled
        const voiceResponseToggle = document.getElementById('voiceResponseToggle');
        if (voiceResponseToggle && voiceResponseToggle.checked && data.voice_url) {
            playVoiceResponse(data.voice_url);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        removeTypingIndicator();
        showNotification('Error sending message. Please try again.', 'danger');
    });
}

/**
 * Add a message to the chat display
 * @param {string} sender - 'user' or 'bot'
 * @param {string} message - The message text
 */
function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageElement = document.createElement('div');
    messageElement.className = sender === 'user' ? 'chat-message user-message' : 'chat-message bot-message';
    
    const avatar = sender === 'user' ? 
        '<div class="avatar"><i class="bi bi-person-circle"></i></div>' : 
        '<div class="avatar"><i class="bi bi-robot"></i></div>';
    
    // Format links in the message
    const formattedMessage = formatMessageLinks(message);
    
    messageElement.innerHTML = `
        ${avatar}
        <div class="message-content">
            <div class="message-text">${formattedMessage}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageElement);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Format links in message text to be clickable
 * @param {string} message - The message text
 * @returns {string} - Formatted message with clickable links
 */
function formatMessageLinks(message) {
    // Regular expression to match URLs
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return message.replace(urlRegex, url => `<a href="${url}" target="_blank">${url}</a>`);
}

/**
 * Add typing indicator to chat
 */
function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    
    const typingElement = document.createElement('div');
    typingElement.className = 'chat-message bot-message typing-indicator';
    typingElement.id = 'typingIndicator';
    
    typingElement.innerHTML = `
        <div class="avatar"><i class="bi bi-robot"></i></div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingElement);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Remove typing indicator from chat
 */
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * Get current time formatted for chat messages
 * @returns {string} - Formatted time string
 */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/**
 * Scroll chat to the bottom
 */
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Play voice response audio
 * @param {string} url - URL of the voice audio file
 */
function playVoiceResponse(url) {
    const audio = new Audio(url);
    audio.play().catch(error => {
        console.error('Error playing audio:', error);
    });
}

/**
 * Clear the chat history
 */
function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    
    // Keep only the welcome message (first child)
    const welcomeMessage = chatMessages.firstChild;
    chatMessages.innerHTML = '';
    
    if (welcomeMessage) {
        chatMessages.appendChild(welcomeMessage);
    }
    
    // Show notification
    showNotification('Chat history cleared', 'info');
}
