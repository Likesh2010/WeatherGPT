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

    localStorage.setItem(
        "weatherGPTLocation",
        JSON.stringify(location)
    );
}


/* =================================
   Get Saved Location
================================= */

function getSavedLocation() {

    try {

        const saved =
            localStorage.getItem("weatherGPTLocation");

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


/* =================================
   Search Location
================================= */

async function searchLocation(location) {

    if (!location || !location.trim()) {

        throw new Error(
            "Please enter a location."
        );
    }

    const response = await fetch(
        `${API_BASE_URL}/weather/current?location=${encodeURIComponent(location)}`
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

                openDashboard({
                    location: data.location,
                    latitude: data.latitude,
                    longitude: data.longitude
                });

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

                saveLocation({

                    location: data.location,

                    latitude:
                        data.latitude,

                    longitude:
                        data.longitude

                });

                if (
                    typeof loadWeatherDashboard ===
                    "function"
                ) {

                    loadWeatherDashboard(
                        data
                    );

                }

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