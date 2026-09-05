/* =================================
   WeatherGPT - App Controller
================================= */

const API_BASE_URL = "/api";


/* =================================
   Utility Functions
================================= */

function showElement(element) {
    if (element) {
        element.classList.remove("hidden");
    }
}


function hideElement(element) {
    if (element) {
        element.classList.add("hidden");
    }
}


function showError(element, message) {
    if (element) {
        element.textContent = message;
    }
}


function clearError(element) {
    if (element) {
        element.textContent = "";
    }
}


/* =================================
   Save Location
================================= */

function saveLocation(location) {

    if (!location) {
        return;
    }

    const normalized = JSON.stringify(location);

    localStorage.setItem(
        "weatherGPTLocation",
        normalized
    );

    localStorage.setItem(
        "weatherLocation",
        normalized
    );
}


/* =================================
   Get Saved Location
================================= */

function getSavedLocation() {

    try {

        const saved =
            localStorage.getItem("weatherGPTLocation") ||
            localStorage.getItem("weatherLocation");

        return saved
            ? JSON.parse(saved)
            : null;

    } catch (error) {

        console.error(
            "Could not read saved location:",
            error
        );

        return null;
    }
}


/* =================================
   Redirect to Dashboard
================================= */

function openDashboard(location) {

    saveLocation(location);

    window.location.href =
        "dashboard.html";
}

function refreshDashboardAfterSearch(data) {
    if (!data) {
        return;
    }

    const locationPayload = {
        location: data.location,
        latitude: data.latitude,
        longitude: data.longitude
    };

    if (typeof loadCurrentWeather === "function") {
        loadCurrentWeather({
            location: data.location,
            latitude: data.latitude,
            longitude: data.longitude
        }).catch((error) => {
            console.error("Dashboard refresh failed:", error);
        });
    }

    if (typeof loadForecast === "function") {
        loadForecast(locationPayload).catch((error) => {
            console.error("Forecast refresh failed:", error);
        });
    }

    if (typeof loadAlerts === "function") {
        loadAlerts(locationPayload).catch((error) => {
            console.error("Alerts refresh failed:", error);
        });
    }
}


/* =================================
   Search Location
================================= */

async function searchLocation(location) {

    const sanitizedLocation = String(location || "").trim();

    if (!sanitizedLocation) {

        throw new Error(
            "Please enter a location."
        );
    }

    const response = await fetch(
        `${API_BASE_URL}/weather/current?location=${encodeURIComponent(sanitizedLocation)}`
    );

    if (!response.ok) {

        throw new Error(
            "Unable to find weather information."
        );
    }

    const result = await response.json();

    if (!result.success) {

        throw new Error(
            result.error?.message ||
            "Location could not be found."
        );
    }

    return result.data;
}


/* =================================
   Home Page
================================= */

function initializeHomePage() {

    const input =
        document.getElementById(
            "locationInput"
        );

    const searchButton =
        document.getElementById(
            "searchButton"
        );

    const currentButton =
        document.getElementById(
            "currentLocationButton"
        );

    const error =
        document.getElementById(
            "searchError"
        );


    if (!input || !searchButton) {
        return;
    }


    searchButton.addEventListener(
        "click",
        async () => {

            clearError(error);

            try {

                searchButton.disabled = true;

                searchButton.textContent =
                    "Searching...";

                const data =
                    await searchLocation(
                        input.value
                    );

                const locationPayload = {
                    location: data.location,
                    latitude: data.latitude,
                    longitude: data.longitude
                };

                saveLocation(locationPayload);

                openDashboard(locationPayload);

            } catch (err) {

                showError(
                    error,
                    err.message
                );

            } finally {

                searchButton.disabled = false;

                searchButton.textContent =
                    "🔍 Search";
            }

        }
    );


    input.addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {

                searchButton.click();

            }

        }
    );


    if (currentButton) {

        currentButton.addEventListener(
            "click",
            () => {

                if (!navigator.geolocation) {

                    showError(
                        error,
                        "Geolocation is not supported by your browser."
                    );

                    return;
                }


                navigator.geolocation.getCurrentPosition(

                    position => {

                        openDashboard({

                            latitude:
                                position.coords.latitude,

                            longitude:
                                position.coords.longitude

                        });

                    },

                    () => {

                        showError(
                            error,
                            "Unable to access your location."
                        );

                    }

                );

            }
        );

    }

}


/* =================================
   Dashboard Search
================================= */

function initializeDashboardSearch() {

    const input =
        document.getElementById(
            "dashboardLocationInput"
        );

    const button =
        document.getElementById(
            "dashboardSearchButton"
        );


    if (!input || !button) {
        return;
    }


    button.addEventListener(
        "click",
        async () => {

            try {

                const data =
                    await searchLocation(
                        input.value
                    );

                const locationPayload = {
                    location: data.location,
                    latitude: data.latitude,
                    longitude: data.longitude
                };

                saveLocation(locationPayload);
                refreshDashboardAfterSearch(locationPayload);

            } catch (error) {

                const errorElement =
                    document.getElementById(
                        "dashboardError"
                    );

                showError(
                    errorElement,
                    error.message
                );

            }

        }
    );


    input.addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {
                event.preventDefault();
                button.click();
            }

        }
    );

}


/* =================================
   Initialize
================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeHomePage();

        initializeDashboardSearch();

    }
);