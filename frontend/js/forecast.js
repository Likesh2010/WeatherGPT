/* =================================
   Forecast
================================= */


async function fetchForecast(location) {

    let url;


    if (
        location.latitude !== undefined &&
        location.longitude !== undefined
    ) {

        url =
            `${API_BASE_URL}/weather/forecast?latitude=${location.latitude}&longitude=${location.longitude}`;

    } else {

        url =
            `${API_BASE_URL}/weather/forecast?location=${encodeURIComponent(location.location)}`;

    }


    const response =
        await fetch(url);


    if (!response.ok) {

        throw new Error(
            "Failed to retrieve forecast."
        );

    }


    const result =
        await response.json();


    if (!result.success) {

        throw new Error(
            result.error?.message ||
            "Forecast unavailable."
        );

    }


    return result.data;

}


/* =================================
   Render Forecast
================================= */

function renderForecast(data) {

    const container =
        document.getElementById(
            "forecastContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    const forecast =
        data.daily ||
        data.forecast ||
        [];


    if (!forecast.length) {

        container.innerHTML = `
            <div class="forecast-placeholder">
                No forecast data available.
            </div>
        `;

        return;

    }


    forecast.forEach(
        item => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "forecast-card";


            const date =
                formatForecastDate(
                    item.date ||
                    item.timestamp
                );


            const temperature =
                item.temperature !== undefined
                    ? `${Math.round(item.temperature)}°C`
                    : "--°C";


            const rain =
                item.rain_probability !== undefined
                    ? `${item.rain_probability}% rain`
                    : "";


            card.innerHTML = `

                <div class="date">
                    ${date}
                </div>

                <img
                    src="${item.icon || ""}"
                    alt="${item.condition || "Weather"}"
                >

                <div class="condition">
                    ${item.condition || "--"}
                </div>

                <div class="forecast-temperature">
                    ${temperature}
                </div>

                <div class="forecast-rain">
                    ${rain}
                </div>

            `;


            container.appendChild(
                card
            );

        }
    );

}


/* =================================
   Date Formatter
================================= */

function formatForecastDate(value) {

    if (!value) {
        return "--";
    }


    const date =
        new Date(value);


    if (Number.isNaN(date.getTime())) {
        return value;
    }


    return date.toLocaleDateString(
        [],
        {
            weekday: "short",
            month: "short",
            day: "numeric"
        }
    );

}


/* =================================
   Forecast Loader
================================= */

async function loadForecast(
    location
) {

    try {

        const data =
            await fetchForecast(
                location
            );


        renderForecast(
            data
        );


        if (
            typeof updateWeatherCharts ===
            "function"
        ) {

            updateWeatherCharts(
                data
            );

        }

    } catch (error) {

        console.error(
            "Forecast error:",
            error
        );

    }

}