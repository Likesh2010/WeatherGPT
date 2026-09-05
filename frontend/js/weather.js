/* =========================================================
   WeatherGPT Current Weather
========================================================= */


/* =========================================================
   Weather Icon
========================================================= */

function setWeatherIcon(element, icon, condition) {

    if (!element) {
        return;
    }

    /*
     * The backend returns an emoji for the weather icon.
     * We use textContent instead of <img src="">
     * so emojis never become broken image URLs.
     */

    const iconValue =
        icon ||
        getWeatherEmoji(condition);

    element.textContent = iconValue;

    element.setAttribute(
        "aria-label",
        condition || "Weather condition"
    );
}


/* =========================================================
   Weather Emoji Fallback
========================================================= */

function getWeatherEmoji(condition) {

    const text =
        String(condition || "")
            .toLowerCase();

    if (
        text.includes("thunder")
    ) {
        return "⛈️";
    }

    if (
        text.includes("rain") ||
        text.includes("drizzle")
    ) {
        return "🌧️";
    }

    if (
        text.includes("snow")
    ) {
        return "❄️";
    }

    if (
        text.includes("fog") ||
        text.includes("mist")
    ) {
        return "🌫️";
    }

    if (
        text.includes("cloud")
    ) {
        return "☁️";
    }

    if (
        text.includes("partly")
    ) {
        return "⛅";
    }

    if (
        text.includes("clear") ||
        text.includes("sun")
    ) {
        return "☀️";
    }

    return "🌤️";
}


/* =========================================================
   Format Number
========================================================= */

function formatNumber(value, decimals = 1) {

    if (
        value === null ||
        value === undefined ||
        value === "" ||
        Number.isNaN(Number(value))
    ) {
        return "--";
    }

    return Number(value).toFixed(decimals);
}


/* =========================================================
   Format Visibility
========================================================= */

function formatVisibility(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "--";
    }

    const numericValue = Number(value);

    if (Number.isNaN(numericValue)) {
        return String(value);
    }

    /*
     * Open-Meteo visibility is returned in metres.
     * Convert metres -> kilometres.
     */

    const kilometers =
        numericValue / 1000;

    return kilometers.toFixed(2);
}


/* =========================================================
   Format Time
========================================================= */

function formatTime(value) {

    if (!value) {
        return "--";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return String(value);
    }

    return date.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


/* =========================================================
   Format Location
========================================================= */

function formatLocationName(data) {

    const location =
        data?.location;

    /*
     * If the backend has a proper location name,
     * use it.
     */

    if (
        location &&
        typeof location === "string" &&
        !location.includes(",")
    ) {
        return location;
    }

    /*
     * If location is already a useful string,
     * use it.
     */

    if (
        location &&
        typeof location === "string" &&
        location.length < 60
    ) {
        return location;
    }

    /*
     * Otherwise display a friendly fallback.
     */

    return "Current Location";
}


/* =========================================================
   Update Weather UI
========================================================= */

function updateWeatherUI(weather) {

    if (!weather) {
        return;
    }


    /* -------------------------
       Location
    ------------------------- */

    const locationName =
        document.getElementById(
            "locationName"
        );

    const locationDetails =
        document.getElementById(
            "locationDetails"
        );


    if (locationName) {

        locationName.textContent =
            formatLocationName(weather);

    }


    if (locationDetails) {

        const latitude =
            Number(weather.latitude);

        const longitude =
            Number(weather.longitude);

        if (
            !Number.isNaN(latitude) &&
            !Number.isNaN(longitude)
        ) {

            locationDetails.textContent =
                `${latitude.toFixed(4)}° N • ` +
                `${longitude.toFixed(4)}° E`;

        } else {

            locationDetails.textContent =
                "Live weather conditions";

        }

    }


    /* -------------------------
       Weather Icon
    ------------------------- */

    const weatherIcon =
        document.getElementById(
            "weatherIcon"
        );

    setWeatherIcon(
        weatherIcon,
        weather.icon,
        weather.condition
    );


    /* -------------------------
       Temperature
    ------------------------- */

    const temperature =
        document.getElementById(
            "temperature"
        );

    if (temperature) {

        temperature.textContent =
            `${formatNumber(weather.temperature, 0)}°C`;

    }


    /* -------------------------
       Condition
    ------------------------- */

    const condition =
        document.getElementById(
            "weatherCondition"
        );

    if (condition) {

        condition.textContent =
            weather.condition || "--";

    }


    /* -------------------------
       Feels Like
    ------------------------- */

    const feelsLike =
        document.getElementById(
            "feelsLike"
        );

    if (feelsLike) {

        feelsLike.textContent =
            `${formatNumber(weather.feels_like, 0)}°C`;

    }


    /* -------------------------
       Humidity
    ------------------------- */

    const humidity =
        document.getElementById(
            "humidity"
        );

    if (humidity) {

        humidity.textContent =
            `${formatNumber(weather.humidity, 0)}%`;

    }


    /* -------------------------
       Wind Speed
    ------------------------- */

    const windSpeed =
        document.getElementById(
            "windSpeed"
        );

    if (windSpeed) {

        windSpeed.textContent =
            `${formatNumber(weather.wind_speed, 1)} km/h`;

    }


    /* -------------------------
       Wind Direction
    ------------------------- */

    const windDirection =
        document.getElementById(
            "windDirection"
        );

    if (windDirection) {

        windDirection.textContent =
            `${formatNumber(weather.wind_direction, 0)}°`;

    }


    /* -------------------------
       Pressure
    ------------------------- */

    const pressure =
        document.getElementById(
            "pressure"
        );

    if (pressure) {

        pressure.textContent =
            `${formatNumber(weather.pressure, 1)} hPa`;

    }


    /* -------------------------
       Visibility
    ------------------------- */

    const visibility =
        document.getElementById(
            "visibility"
        );

    if (visibility) {

        visibility.textContent =
            `${formatVisibility(weather.visibility)} km`;

    }


    /* -------------------------
       UV Index
    ------------------------- */

    const uvIndex =
        document.getElementById(
            "uvIndex"
        );

    if (uvIndex) {

        uvIndex.textContent =
            formatNumber(weather.uv, 1);

    }


    /* -------------------------
       Sunrise
    ------------------------- */

    const sunrise =
        document.getElementById(
            "sunrise"
        );

    if (sunrise) {

        sunrise.textContent =
            formatTime(weather.sunrise);

    }


    /* -------------------------
       Sunset
    ------------------------- */

    const sunset =
        document.getElementById(
            "sunset"
        );

    if (sunset) {

        sunset.textContent =
            formatTime(weather.sunset);

    }


    /* -------------------------
       Precipitation
    ------------------------- */

    const precipitation =
        document.getElementById(
            "precipitation"
        );

    if (precipitation) {

        precipitation.textContent =
            `${formatNumber(
                weather.precipitation,
                1
            )} mm`;

    }


    /* -------------------------
       Updated Time
    ------------------------- */

    const updatedTime =
        document.getElementById(
            "updatedTime"
        );

    if (updatedTime) {

        updatedTime.textContent =
            formatTime(
                weather.timestamp
            );

    }


    /* -------------------------
       Risk
    ------------------------- */

    if (weather.risk) {

        updateRiskUI(
            weather.risk
        );

    }

}


/* =========================================================
   Update Risk UI
========================================================= */

function updateRiskUI(risk) {

    if (!risk) {
        return;
    }

    updateRiskElement(
        "overallRisk",
        risk.overall
    );

    updateRiskElement(
        "heatRisk",
        risk.heat
    );

    updateRiskElement(
        "rainRisk",
        risk.rain
    );

    updateRiskElement(
        "windRisk",
        risk.wind
    );

    updateRiskElement(
        "floodRisk",
        risk.flood
    );

    updateRiskDescription(
        "heatRiskDescription",
        risk.heat
    );

    updateRiskDescription(
        "rainRiskDescription",
        risk.rain
    );

    updateRiskDescription(
        "windRiskDescription",
        risk.wind
    );

    updateRiskDescription(
        "floodRiskDescription",
        risk.flood
    );

}


/* =========================================================
   Risk Element
========================================================= */

function updateRiskElement(
    elementId,
    riskData
) {

    const element =
        document.getElementById(
            elementId
        );

    if (!element || !riskData) {
        return;
    }

    const level =
        String(
            riskData.level ||
            "UNKNOWN"
        ).toUpperCase();

    element.textContent = level;

    element.classList.remove(
        "risk-low",
        "risk-moderate",
        "risk-high",
        "risk-extreme",
        "risk-unknown"
    );

    element.classList.add(
        `risk-${level.toLowerCase()}`
    );

}


/* =========================================================
   Risk Description
========================================================= */

function updateRiskDescription(
    elementId,
    riskData
) {

    const element =
        document.getElementById(
            elementId
        );

    if (!element || !riskData) {
        return;
    }

    element.textContent =
        riskData.description ||
        "No significant risk detected.";

}


/* =========================================================
   Fetch Current Weather
========================================================= */

async function loadCurrentWeather(
    params = {}
) {

    const loading =
        document.getElementById(
            "dashboardLoading"
        );

    const error =
        document.getElementById(
            "dashboardError"
        );


    if (loading) {
        loading.classList.remove("hidden");
    }

    if (error) {
        error.textContent = "";
    }


    try {

        let query = "";


        if (params.location) {

            query =
                `?location=${encodeURIComponent(
                    params.location
                )}`;

        }

        else if (
            params.latitude !== undefined &&
            params.longitude !== undefined
        ) {

            query =
                `?latitude=${encodeURIComponent(
                    params.latitude
                )}&longitude=${encodeURIComponent(
                    params.longitude
                )}`;

        }

        else {

            throw new Error(
                "No location provided."
            );

        }


        const response =
            await fetch(
                `/api/weather/current${query}`
            );


        const result =
            await response.json();


        if (!response.ok || !result.success) {

            throw new Error(
                result?.error?.message ||
                "Unable to load weather data."
            );

        }


        const weather =
            result.data;


        updateWeatherUI(
            weather
        );


        /*
         * Store location for other dashboard components.
         */

        if (
            weather.latitude !== undefined &&
            weather.longitude !== undefined
        ) {

            localStorage.setItem(
                "weatherLatitude",
                weather.latitude
            );

            localStorage.setItem(
                "weatherLongitude",
                weather.longitude
            );
        }

        if (weather.location) {
            localStorage.setItem(
                "weatherLocation",
                JSON.stringify({
                    location: weather.location,
                    latitude: weather.latitude,
                    longitude: weather.longitude
                })
            );

            localStorage.setItem(
                "weatherGPTLocation",
                JSON.stringify({
                    location: weather.location,
                    latitude: weather.latitude,
                    longitude: weather.longitude
                })
            );
        }


        return weather;


    }

    catch (errorObject) {

        console.error(
            "Weather loading error:",
            errorObject
        );


        if (error) {

            error.textContent =
                errorObject.message ||
                "Unable to load weather data.";

        }

        throw errorObject;


    }

    finally {

        if (loading) {
            loading.classList.add("hidden");
        }

    }

}


/* =========================================================
   Dashboard Initial Load
========================================================= */

async function initializeDashboard() {

    try {

        const savedLocation =
            localStorage.getItem(
                "weatherLocation"
            );

        const savedLatitude =
            localStorage.getItem(
                "weatherLatitude"
            );

        const savedLongitude =
            localStorage.getItem(
                "weatherLongitude"
            );


        if (savedLocation) {

            const parsedLocation =
                savedLocation.startsWith("{")
                    ? JSON.parse(savedLocation)
                    : { location: savedLocation };

            await loadCurrentWeather(parsedLocation);
            if (typeof loadForecast === "function") {
                await loadForecast(parsedLocation);
            }
            if (typeof loadAlerts === "function") {
                await loadAlerts(parsedLocation);
            }
            return;

        }


        if (
            savedLatitude &&
            savedLongitude
        ) {

            const params = {
                latitude: savedLatitude,
                longitude: savedLongitude
            };

            await loadCurrentWeather(params);
            if (typeof loadForecast === "function") {
                await loadForecast(params);
            }
            if (typeof loadAlerts === "function") {
                await loadAlerts(params);
            }
            return;

        }


        /*
         * Default location for development.
         */

        const defaultLocation = { location: "Chennai" };

        await loadCurrentWeather(defaultLocation);
        if (typeof loadForecast === "function") {
            await loadForecast(defaultLocation);
        }
        if (typeof loadAlerts === "function") {
            await loadAlerts(defaultLocation);
        }


    }

    catch (error) {

        console.error(
            "Dashboard initialization failed:",
            error
        );

    }

}


/* =========================================================
   Start Dashboard
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeDashboard();

    }
);