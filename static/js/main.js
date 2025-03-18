/**
 * Ulimi Wise - Main JavaScript file
 * Contains common functionality used across the application
 */

// Global variables
let currentLanguage = 'en';
let translations = {};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Ulimi Wise application initialized');
    
    // Set current language from HTML lang attribute or local storage
    currentLanguage = document.documentElement.lang || localStorage.getItem('language') || 'en';
    
    // Initialize language selector
    initLanguageSelector();
    
    // Initialize UI components
    initTooltips();
    initToasts();
    initPopovers();
    
    // Initialize voice input for chatbot if on chatbot page
    if (document.getElementById('voiceInputBtn')) {
        initVoiceInput();
    }
    
    // Check if weather widget exists and initialize it
    if (document.getElementById('weatherWidget')) {
        loadWeatherData();
    }
});

/**
 * Initialize language selector dropdown
 */
function initLanguageSelector() {
    const languageSelector = document.getElementById('languageSelector');
    if (languageSelector) {
        // Update the selected language in the dropdown
        const options = languageSelector.querySelectorAll('option');
        options.forEach(option => {
            if (option.value === currentLanguage) {
                option.selected = true;
            }
        });
        
        // Add event listener for language change
        languageSelector.addEventListener('change', function(e) {
            const newLanguage = e.target.value;
            changeLanguage(newLanguage);
        });
    }
}

/**
 * Change the application language
 * @param {string} langCode - The language code to change to
 */
function changeLanguage(langCode) {
    // Store language preference
    localStorage.setItem('language', langCode);
    
    // Redirect to language change endpoint
    window.location.href = `/set_language/${langCode}`;
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            boundary: document.body
        });
    });
}

/**
 * Initialize Bootstrap toasts
 */
function initToasts() {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
    });
    
    // Show all toasts
    toastElList.forEach(toast => {
        const bsToast = bootstrap.Toast.getInstance(toast);
        if (bsToast) {
            bsToast.show();
        } else {
            const newToast = new bootstrap.Toast(toast);
            newToast.show();
        }
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Show a notification toast
 * @param {string} message - The message to display
 * @param {string} type - The type of toast (success, danger, warning, info)
 */
function showNotification(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        console.error('Toast container not found');
        return;
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    // Append the toast to the container
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Show the toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    toast.show();
    
    // Remove the toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Load weather data for the current user's location or provided location
 * @param {string} location - Optional location to load weather for
 */
function loadWeatherData(location = '') {
    const weatherWidget = document.getElementById('weatherWidget');
    if (!weatherWidget) return;
    
    // Show loading state
    weatherWidget.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Use location parameter or get from input field
    if (!location) {
        const locationInput = document.getElementById('locationInput');
        if (locationInput) {
            location = locationInput.value;
        }
    }
    
    // Make API request to get weather data
    fetch(`/weather?location=${encodeURIComponent(location)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateWeatherWidget(data);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            weatherWidget.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Unable to load weather data. Please check your location settings.
                </div>
            `;
        });
}

/**
 * Update the weather widget with the weather data
 * @param {Object} data - Weather data from the API
 */
function updateWeatherWidget(data) {
    const weatherWidget = document.getElementById('weatherWidget');
    if (!weatherWidget) return;
    
    if (!data.weather) {
        weatherWidget.innerHTML = `
            <div class="alert alert-warning" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                No weather data available for this location.
            </div>
        `;
        return;
    }
    
    const weather = data.weather;
    const recommendations = data.recommendations || [];
    
    // Build weather HTML
    let weatherHTML = `
        <div class="card shadow-sm">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                    <i class="bi bi-geo-alt-fill me-2"></i>
                    ${weather.location}
                </h5>
                <span class="text-muted small">${weather.timestamp}</span>
            </div>
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-6 text-center">
                        <div class="display-4 mb-2">${weather.temperature.current}°C</div>
                        <div class="text-muted">Feels like: ${weather.temperature.feels_like}°C</div>
                        <div class="my-2">
                            <img src="https://openweathermap.org/img/wn/${weather.icon}@2x.png" alt="${weather.description}" width="80">
                            <div>${weather.description}</div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-thermometer-half me-2"></i>Min/Max</span>
                                <span>${weather.temperature.min}°C / ${weather.temperature.max}°C</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-droplet-half me-2"></i>Humidity</span>
                                <span>${weather.humidity}%</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-wind me-2"></i>Wind</span>
                                <span>${weather.wind.speed} m/s</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-sun me-2"></i>Sunrise</span>
                                <span>${weather.sunrise}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-moon me-2"></i>Sunset</span>
                                <span>${weather.sunset}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
    `;
    
    // Add recommendations if available
    if (recommendations.length > 0) {
        weatherHTML += `
            <div class="card-footer bg-light">
                <h6><i class="bi bi-lightbulb-fill me-2"></i>Recommendations:</h6>
                <ul class="list-group list-group-flush">
        `;
        
        recommendations.forEach(recommendation => {
            weatherHTML += `
                <li class="list-group-item bg-transparent">${recommendation}</li>
            `;
        });
        
        weatherHTML += `
                </ul>
            </div>
        `;
    }
    
    weatherHTML += `</div>`;
    
    // Update the widget
    weatherWidget.innerHTML = weatherHTML;
}

/**
 * Initialize voice input for chatbot
 */
function initVoiceInput() {
    const voiceInputBtn = document.getElementById('voiceInputBtn');
    if (!voiceInputBtn) return;
    
    // Check if browser supports SpeechRecognition
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // Set recognition properties
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = currentLanguage;
        
        // Add event listeners for recognition
        recognition.onstart = function() {
            voiceInputBtn.classList.add('btn-danger');
            voiceInputBtn.innerHTML = '<i class="bi bi-mic-fill"></i> Listening...';
        };
        
        recognition.onresult = function(event) {
            const speechResult = event.results[0][0].transcript;
            document.getElementById('messageInput').value = speechResult;
            
            // Send the message automatically
            sendMessage();
        };
        
        recognition.onend = function() {
            voiceInputBtn.classList.remove('btn-danger');
            voiceInputBtn.innerHTML = '<i class="bi bi-mic"></i> Speak';
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error', event.error);
            voiceInputBtn.classList.remove('btn-danger');
            voiceInputBtn.innerHTML = '<i class="bi bi-mic"></i> Speak';
            showNotification('Speech recognition failed. Please try again or type your message.', 'warning');
        };
        
        // Start recognition when button is clicked
        voiceInputBtn.addEventListener('click', function() {
            recognition.start();
        });
    } else {
        // Browser doesn't support speech recognition
        voiceInputBtn.disabled = true;
        voiceInputBtn.title = 'Speech recognition not supported in this browser';
        showNotification('Speech recognition is not supported in your browser. Please type your messages.', 'warning');
    }
}

/**
 * Format a date string
 * @param {string} dateString - The date string to format
 * @returns {string} - Formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString(currentLanguage, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format currency based on locale
 * @param {number} amount - The amount to format
 * @returns {string} - Formatted currency string
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat(currentLanguage, {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}
