// ============================================================
// WeatherGPT - Weather Map
// ============================================================

let weatherMap = null;
let weatherMarker = null;


// ============================================================
// INITIALIZE MAP
// ============================================================

function initializeWeatherMap() {

    const mapElement = document.getElementById("weatherMap");

    if (!mapElement) {
        console.warn("weatherMap element not found.");
        return;
    }

    // Prevent duplicate initialization
    if (weatherMap) {
        return;
    }

    // Default location: Chennai
    const defaultLatitude = 13.0827;
    const defaultLongitude = 80.2707;

    weatherMap = L.map("weatherMap").setView(
        [defaultLatitude, defaultLongitude],
        10
    );

    // OpenStreetMap tiles
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/">' +
                'OpenStreetMap</a> contributors',

            maxZoom: 19
        }
    ).addTo(weatherMap);

    // Default marker
    weatherMarker = L.marker([
        defaultLatitude,
        defaultLongitude
    ]).addTo(weatherMap);

    weatherMarker.bindPopup(
        "WeatherGPT<br>Chennai"
    );

    // Fix Leaflet rendering issues
    setTimeout(() => {
        weatherMap.invalidateSize();
    }, 300);
}


// ============================================================
// SEARCH LOCATION
// ============================================================

async function searchMapLocation() {

    const input = document.getElementById(
        "mapLocationInput"
    );

    const errorElement = document.getElementById(
        "mapError"
    );

    if (!input) {
        return;
    }

    const location = input.value.trim();

    // Clear previous error
    if (errorElement) {
        errorElement.textContent = "";
        errorElement.style.display = "none";
    }

    // Validate input
    if (!location) {

        showMapError(
            "Please enter a city or location."
        );

        return;
    }

    // Show loading state
    const searchButton = document.getElementById(
        "mapSearchButton"
    );

    if (searchButton) {

        searchButton.disabled = true;
        searchButton.textContent = "Searching...";
    }

    try {

        const url =
            `/api/weather/map?location=${encodeURIComponent(location)}`;

        const response = await fetch(url);

        const result = await response.json();

        console.log("Map API response:", result);

        // API failure
        if (!response.ok || !result.success) {

            const message =
                result?.error?.message ||
                "Unable to find weather information.";

            throw new Error(message);
        }

        const weather = result.data;

        if (
            weather.latitude === undefined ||
            weather.longitude === undefined
        ) {

            throw new Error(
                "Location coordinates were not returned."
            );
        }

        // Update map
        updateWeatherMap(weather);

        // Update information panel
        updateMapWeatherInfo(weather);

    }

    catch (error) {

        console.error(
            "Map search error:",
            error
        );

        showMapError(
            error.message ||
            "Unable to find weather information."
        );
    }

    finally {

        if (searchButton) {

            searchButton.disabled = false;
            searchButton.textContent = "Search";
        }
    }
}


// ============================================================
// UPDATE MAP
// ============================================================

function updateWeatherMap(weather) {

    if (!weatherMap) {
        initializeWeatherMap();
    }

    if (!weatherMap) {
        return;
    }

    const latitude = Number(
        weather.latitude
    );

    const longitude = Number(
        weather.longitude
    );

    if (
        !Number.isFinite(latitude) ||
        !Number.isFinite(longitude)
    ) {

        showMapError(
            "Invalid coordinates received from server."
        );

        return;
    }

    // Move map
    weatherMap.setView(
        [latitude, longitude],
        10,
        {
            animate: true
        }
    );

    // Remove old marker
    if (weatherMarker) {

        weatherMap.removeLayer(
            weatherMarker
        );
    }

    // Create new marker
    weatherMarker = L.marker([
        latitude,
        longitude
    ]).addTo(weatherMap);

    // Build popup
    const locationName =
        weather.location ||
        "Selected Location";

    const temperature =
        weather.temperature !== undefined
            ? `${weather.temperature}°C`
            : "N/A";

    const condition =
        weather.condition ||
        "Unknown";

    const humidity =
        weather.humidity !== undefined
            ? `${weather.humidity}%`
            : "N/A";

    const wind =
        weather.wind_speed !== undefined
            ? `${weather.wind_speed} km/h`
            : "N/A";

    const popupHTML = `
        <div class="map-popup">
            <strong>${escapeHTML(locationName)}</strong>

            <br><br>

            🌡️ Temperature:
            ${escapeHTML(String(temperature))}

            <br>

            ☁️ Condition:
            ${escapeHTML(String(condition))}

            <br>

            💧 Humidity:
            ${escapeHTML(String(humidity))}

            <br>

            💨 Wind:
            ${escapeHTML(String(wind))}
        </div>
    `;

    weatherMarker
        .bindPopup(popupHTML)
        .openPopup();

    // Fix map size
    setTimeout(() => {

        weatherMap.invalidateSize();

    }, 300);
}


// ============================================================
// UPDATE WEATHER INFORMATION
// ============================================================

function updateMapWeatherInfo(weather) {

    const locationElement =
        document.getElementById(
            "mapLocation"
        );

    const coordinatesElement =
        document.getElementById(
            "mapCoordinates"
        );

    const temperatureElement =
        document.getElementById(
            "mapTemperature"
        );

    const conditionElement =
        document.getElementById(
            "mapCondition"
        );

    if (locationElement) {

        locationElement.textContent =
            weather.location ||
            "Selected Location";
    }

    if (coordinatesElement) {

        const latitude =
            Number(weather.latitude).toFixed(4);

        const longitude =
            Number(weather.longitude).toFixed(4);

        coordinatesElement.textContent =
            `${latitude}, ${longitude}`;
    }

    if (temperatureElement) {

        temperatureElement.textContent =
            weather.temperature !== undefined
                ? `${weather.temperature}°C`
                : "--";
    }

    if (conditionElement) {

        conditionElement.textContent =
            weather.condition ||
            "Unknown";
    }
}


// ============================================================
// SHOW ERROR
// ============================================================

function showMapError(message) {

    const errorElement =
        document.getElementById(
            "mapError"
        );

    if (!errorElement) {
        return;
    }

    errorElement.textContent =
        message;

    errorElement.style.display =
        "block";
}


// ============================================================
// ENTER KEY SEARCH
// ============================================================

function setupMapSearch() {

    const input =
        document.getElementById(
            "mapLocationInput"
        );

    const button =
        document.getElementById(
            "mapSearchButton"
        );

    if (button) {

        button.addEventListener(
            "click",
            searchMapLocation
        );
    }

    if (input) {

        input.addEventListener(
            "keydown",
            function (event) {

                if (event.key === "Enter") {

                    event.preventDefault();

                    searchMapLocation();
                }
            }
        );
    }
}


// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeWeatherMap();

        setupMapSearch();
    }
);