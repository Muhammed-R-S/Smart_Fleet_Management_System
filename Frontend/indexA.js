const themeToggler = document.querySelector(".theme-toggler");

// Change theme
themeToggler.addEventListener('click', () => {
    const isDarkTheme = document.body.classList.contains('dark-theme-variables');
    const spans = themeToggler.querySelectorAll('span');

    if (isDarkTheme && spans[0].classList.contains('active')) {
        return;
    } else if (!isDarkTheme && spans[1].classList.contains('active')) {
        return;
    }

    if (isDarkTheme) {
        document.body.classList.remove('dark-theme-variables');
    } else {
        document.body.classList.add('dark-theme-variables');
    }

    updateThemeButtons();
});

// Function to update the active state of the theme toggler buttons
function updateThemeButtons() {
    const spans = themeToggler.querySelectorAll('span');
    spans.forEach(span => {
        span.classList.remove('active');
    });

    if (document.body.classList.contains('dark-theme-variables')) {
        spans[1].classList.add('active');
    } else {
        spans[0].classList.add('active');
    }
}

updateThemeButtons();


// WebSocket connection for latest data
const socketLatestData = new WebSocket('ws://localhost:8000');
socketLatestData.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if ('latest_vehicle_data' in data) {
        updateDashboard(data.latest_vehicle_data); // Update the dashboard with latest data
    }
};

// Function to update the dashboard with received data
function updateDashboard(data) {
    // Update the HTML elements in the dashboard with the received data
    document.getElementById('fuel_level').innerText = data.fuel_level + ' Litre';
    document.getElementById('speed_level').innerText = data.speed_level + ' Km/h';
    document.getElementById('temperature').innerText = data.temperature + ' °C';

    // Calculate the engine rating based on the temperature
    var temperature = data.temperature;
    var engineRating = '';

    if (temperature < 60) {
        engineRating = 'Excellent';
    } else if (temperature >= 60 && temperature <= 80) {
        engineRating = 'Good';
    } else if (temperature >= 81 && temperature <= 100) {
        engineRating = 'Average';
    } else if (temperature >= 101 && temperature <= 120) {
        engineRating = 'Bad';
    } else {
        engineRating = 'Very Bad';
    }

    // Update the engine rating element
    document.getElementById('engine_rating').innerText = engineRating;

    // Update the engine status to "Off" if data hasn't been updated for 15 seconds
    const currentTime = Date.now();
    const lastUpdateTime = parseInt(localStorage.getItem('lastUpdateTime')) || 0;
    const timeDiff = currentTime - lastUpdateTime;
    const updateInterval = 15 * 1000; // 15 seconds in milliseconds

    if (timeDiff > updateInterval) {
        document.getElementById('engine_status').innerText = 'Off';
    } else {
        document.getElementById('engine_status').innerText = 'On';
    }

    // Update the fuel alerts count and element
    const fuelAlerts = data.fuel_alerts || 0;
    document.getElementById('fuel_alerts').innerText = fuelAlerts + ' fuel alerts';

    // Update the last update time
    localStorage.setItem('lastUpdateTime', currentTime.toString());
}

