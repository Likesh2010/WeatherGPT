/* =================================
   Weather Data
================================= */


async function fetchCurrentWeather(location) {

    let url;


    if (
        location.latitude !== undefined &&
        location.longitude !== undefined
    ) {

        url =
            `${API_BASE_URL}/weather/current?latitude=${location.latitude}&longitude=${location.longitude}`;

    } else {

        url =
            `${API_BASE_URL}/weather/current?location=${encodeURIComponent(location.location)}`;

    }


    const response =
        await fetch(url);


    if (!response.ok) {

        throw new Error(
            "Failed to retrieve current weather."
        );

    }


    const result =
        await response.json();


    if (!result.success) {

        throw new Error(
            result.error?.message ||
            "Weather data unavailable."
        );

    }


    return result.data;

}


/* =================================
   Update Current Weather UI
================================= */

function updateCurrentWeather(data) {

    if (!data) {
        return;
    }


    const setText =
        (id, value) => {

            const element =
                document.getElementById(id);

            if (element) {
                element.textContent =
                    value ?? "--";
            }

        };


    setText(
        "locationName",
        data.location || "Unknown Location"
    );


    setText(
        "locationDetails",

        data.latitude !== undefined &&
        data.longitude !== undefined

            ? `Latitude: ${data.latitude} | Longitude: ${data.longitude}`

            : ""
    );


    setText(
        "temperature",

        data.temperature !== undefined
            ? `${Math.round(data.temperature)}°C`
            : "--°C"
    );


    setText(
        "feelsLike",

        data.feels_like !== undefined
            ? `${Math.round(data.feels_like)}°C`
            : "--°C"
    );


    setText(
        "weatherCondition",
        data.condition || "--"
    );


    setText(
        "humidity",

        data.humidity !== undefined
            ? `${data.humidity}%`
            : "--%"
    );


    setText(
        "windSpeed",

        data.wind_speed !== undefined
            ? `${data.wind_speed} km/h`
            : "-- km/h"
    );


    setText(
        "windDirection",

        data.wind_direction !== undefined
            ? `${data.wind_direction}°`
            : "--"
    );


    setText(
        "pressure",

        data.pressure !== undefined
            ? `${data.pressure} hPa`
            : "-- hPa"
    );


    setText(
        "visibility",

        data.visibility !== undefined
            ? `${data.visibility} km`
            : "-- km"
    );


    setText(
        "uvIndex",

        data.uv !== undefined
            ? data.uv
            : "--"
    );


    setText(
        "precipitation",

        data.precipitation !== undefined
            ? `${data.precipitation} mm`
            : "-- mm"
    );


    setText(
        "sunrise",
        formatTime(data.sunrise)
    );


    setText(
        "sunset",
        formatTime(data.sunset)
    );


    setText(
        "updatedTime",
        formatTime(data.timestamp)
    );


    const icon =
        document.getElementById(
            "weatherIcon"
        );


    if (icon && data.icon) {

        icon.src = data.icon;

        icon.alt =
            data.condition ||
            "Weather";

    }

}


/* =================================
   Time Formatter
================================= */

function formatTime(value) {

    if (!value) {
        return "--";
    }


    const date =
        new Date(value);


    if (Number.isNaN(date.getTime())) {
        return value;
    }


    return date.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


/* =================================
   Dashboard Loader
================================= */

async function loadWeatherDashboard(
    locationData = null
) {

    const loading =
        document.getElementById(
            "dashboardLoading"
        );

    const error =
        document.getElementById(
            "dashboardError"
        );


    try {

        hideElement(error);

        showElement(loading);


        const location =
            locationData ||
            getSavedLocation();


        if (!location) {

            throw new Error(
                "Please search for a location first."
            );

        }


        const weather =
            await fetchCurrentWeather(
                location
            );


        updateCurrentWeather(
            weather
        );


        if (
            typeof loadForecast ===
            "function"
        ) {

            loadForecast(
                weather
            );

        }


        if (
            typeof loadAlerts ===
            "function"
        ) {

            loadAlerts(
                weather
            );

        }


        if (
            typeof loadRiskAnalysis ===
            "function"
        ) {

            loadRiskAnalysis(
                weather
            );

        }


        if (
            typeof initializeWeatherMap ===
            "function"
        ) {

            initializeWeatherMap(
                weather.latitude,
                weather.longitude,
                weather
            );

        }


    } catch (err) {

        showError(
            error,
            err.message
        );

    } finally {

        hideElement(loading);

    }

}


/* =================================
   Dashboard Initialization
================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (
            document.getElementById(
                "temperature"
            )
        ) {

            loadWeatherDashboard();

        }

    }
);