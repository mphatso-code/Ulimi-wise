/**
 * Ulimi Wise - Weather JavaScript
 * Handles weather data fetching and display
 */

// Define current language variable or get it from main.js if available
let currentLanguage = 'en';
if (typeof window.currentLanguage !== 'undefined') {
    currentLanguage = window.currentLanguage;
} else {
    // Try to get language from HTML lang attribute or localStorage
    currentLanguage = document.documentElement.lang || localStorage.getItem('language') || 'en';
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Weather script loaded');
    
    // Initialize location search
    initLocationSearch();
    
    // Initialize refresh button
    initRefreshWeather();
});

/**
 * Initialize location search functionality
 */
function initLocationSearch() {
    const locationForm = document.getElementById('locationSearchForm');
    if (locationForm) {
        locationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const location = document.getElementById('locationInput').value.trim();
            if (location) {
                loadWeatherData(location);
            }
        });
    }
}

/**
 * Initialize weather refresh button
 */
function initRefreshWeather() {
    const refreshButton = document.getElementById('refreshWeatherBtn');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            const location = document.getElementById('locationInput').value.trim();
            loadWeatherData(location);
        });
    }
}

/**
 * Get weather forecast for the specified location
 * @param {string} location - Location to get forecast for
 */
function getWeatherForecast(location) {
    const forecastContainer = document.getElementById('weatherForecast');
    if (!forecastContainer) return;
    
    // Show loading state
    forecastContainer.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Make API request to get forecast data
    fetch(`/weather/forecast?location=${encodeURIComponent(location)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateWeatherForecast(data);
        })
        .catch(error => {
            console.error('Error fetching weather forecast:', error);
            forecastContainer.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Unable to load weather forecast. Please try again later.
                </div>
            `;
        });
}

/**
 * Update the weather forecast display
 * @param {Object} data - Forecast data from the API
 */
function updateWeatherForecast(data) {
    const forecastContainer = document.getElementById('weatherForecast');
    if (!forecastContainer) return;
    
    if (!data.forecast || data.forecast.length === 0) {
        forecastContainer.innerHTML = `
            <div class="alert alert-warning" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                No forecast data available for this location.
            </div>
        `;
        return;
    }
    
    let forecastHTML = '<div class="row">';
    
    data.forecast.forEach(day => {
        let iconClass = 'bi-cloud';
        
        // Set appropriate icon based on condition
        if (day.main_condition) {
            const condition = day.main_condition.toLowerCase();
            if (condition.includes('clear')) {
                iconClass = 'bi-sun';
            } else if (condition.includes('rain')) {
                iconClass = 'bi-cloud-rain';
            } else if (condition.includes('snow')) {
                iconClass = 'bi-snow';
            } else if (condition.includes('thunder')) {
                iconClass = 'bi-lightning';
            } else if (condition.includes('cloud')) {
                iconClass = 'bi-cloudy';
            } else if (condition.includes('fog') || condition.includes('mist')) {
                iconClass = 'bi-cloud-fog';
            }
        }
        
        // Format date
        const date = new Date(day.date);
        const formattedDate = date.toLocaleDateString(currentLanguage, {
            weekday: 'short',
            month: 'short',
            day: 'numeric'
        });
        
        forecastHTML += `
            <div class="col-md-4 col-sm-6 mb-3">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <h5 class="card-title">${formattedDate}</h5>
                        <div class="my-3">
                            <i class="bi ${iconClass} display-4"></i>
                            <div>${day.main_condition}</div>
                        </div>
                        <div class="row">
                            <div class="col-6">
                                <div class="text-primary">
                                    <i class="bi bi-thermometer-high"></i> ${Math.round(day.temperature.max)}°C
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="text-info">
                                    <i class="bi bi-thermometer-low"></i> ${Math.round(day.temperature.min)}°C
                                </div>
                            </div>
                        </div>
                        <div class="mt-2">
                            <i class="bi bi-droplet"></i> Precip: ${day.precipitation.toFixed(1)} mm
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    forecastHTML += '</div>';
    
    // Update the container
    forecastContainer.innerHTML = forecastHTML;
}

/**
 * Save location as default for user
 * @param {string} location - Location to save
 */
function saveDefaultLocation(location) {
    if (!location.trim()) return;
    
    const formData = new FormData();
    formData.append('location', location);
    
    fetch('/profile/update_location', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showNotification('Default location updated successfully', 'success');
        } else {
            showNotification(data.error || 'Error updating location', 'danger');
        }
    })
    .catch(error => {
        console.error('Error saving location:', error);
        showNotification('Error saving location. Please try again.', 'danger');
    });
}
