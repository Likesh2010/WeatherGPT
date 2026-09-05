/* =========================================================
   WeatherGPT Charts
========================================================= */

let temperatureChart = null;
let rainChart = null;
let humidityChart = null;
let windChart = null;


/* =========================================================
   Get Forecast Data
========================================================= */

function getChartData(data) {

    if (!data) {
        return [];
    }

    if (Array.isArray(data)) {
        return data;
    }

    if (Array.isArray(data.hourly)) {
        return data.hourly;
    }

    if (Array.isArray(data.forecast)) {
        return data.forecast;
    }

    if (data.data) {
        if (Array.isArray(data.data)) {
            return data.data;
        }

        if (Array.isArray(data.data.hourly)) {
            return data.data.hourly;
        }

        if (Array.isArray(data.data.forecast)) {
            return data.data.forecast;
        }
    }

    return [];
}


/* =========================================================
   Get Value From Multiple Possible Names
========================================================= */

function getValue(item, keys) {

    for (const key of keys) {

        if (
            item &&
            item[key] !== undefined &&
            item[key] !== null
        ) {
            return item[key];
        }

    }

    return null;
}


/* =========================================================
   Format Chart Time
========================================================= */

function formatChartTime(value) {

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
            hour: "numeric",
            minute: "2-digit"
        }
    );
}


/* =========================================================
   Destroy Chart
========================================================= */

function destroyChart(chart) {

    if (chart) {
        chart.destroy();
    }

}


/* =========================================================
   Common Chart Options
========================================================= */

function getCommonOptions() {

    return {

        responsive: true,

        maintainAspectRatio: false,

        animation: {
            duration: 500
        },

        plugins: {

            legend: {
                display: true,

                position: "top",

                labels: {
                    boxWidth: 10,

                    usePointStyle: true
                }
            }

        },

        interaction: {
            intersect: false,

            mode: "index"
        }

    };

}


/* =========================================================
   Temperature Chart
========================================================= */

function createTemperatureChart(data) {

    const canvas =
        document.getElementById(
            "temperatureChart"
        );

    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    const items = getChartData(data);

    const labels = items.map(
        item =>
            formatChartTime(
                getValue(item, [
                    "timestamp",
                    "time",
                    "date"
                ])
            )
    );

    const values = items.map(
        item =>
            getValue(item, [
                "temperature",
                "temperature_2m",
                "temp"
            ])
    );

    destroyChart(temperatureChart);

    temperatureChart = new Chart(
        canvas,
        {
            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {
                        label: "Temperature (°C)",

                        data: values,

                        tension: 0.35,

                        fill: true,

                        pointRadius: 2,

                        pointHoverRadius: 5
                    }

                ]

            },

            options: {

                ...getCommonOptions(),

                scales: {

                    x: {
                        grid: {
                            display: false
                        }
                    },

                    y: {

                        beginAtZero: false,

                        title: {
                            display: true,
                            text: "°C"
                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   Rain Chart
========================================================= */

function createRainChart(data) {

    const canvas =
        document.getElementById(
            "rainChart"
        );

    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    const items = getChartData(data);

    const labels = items.map(
        item =>
            formatChartTime(
                getValue(item, [
                    "timestamp",
                    "time",
                    "date"
                ])
            )
    );

    const values = items.map(
        item =>
            getValue(item, [
                "precipitation",
                "precipitation_sum",
                "rain"
            ]) ?? 0
    );

    destroyChart(rainChart);

    rainChart = new Chart(
        canvas,
        {
            type: "bar",

            data: {

                labels: labels,

                datasets: [

                    {
                        label: "Precipitation (mm)",

                        data: values,

                        borderRadius: 5
                    }

                ]

            },

            options: {

                ...getCommonOptions(),

                scales: {

                    x: {
                        grid: {
                            display: false
                        }
                    },

                    y: {

                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "mm"
                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   Humidity Chart
========================================================= */

function createHumidityChart(data) {

    const canvas =
        document.getElementById(
            "humidityChart"
        );

    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    const items = getChartData(data);

    const labels = items.map(
        item =>
            formatChartTime(
                getValue(item, [
                    "timestamp",
                    "time",
                    "date"
                ])
            )
    );

    const values = items.map(
        item =>
            getValue(item, [
                "humidity",
                "relative_humidity",
                "relative_humidity_2m"
            ])
    );

    destroyChart(humidityChart);

    humidityChart = new Chart(
        canvas,
        {
            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {
                        label: "Humidity (%)",

                        data: values,

                        tension: 0.35,

                        pointRadius: 2,

                        pointHoverRadius: 5
                    }

                ]

            },

            options: {

                ...getCommonOptions(),

                scales: {

                    x: {
                        grid: {
                            display: false
                        }
                    },

                    y: {

                        min: 0,

                        max: 100,

                        title: {
                            display: true,
                            text: "%"
                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   Wind Chart
========================================================= */

function createWindChart(data) {

    const canvas =
        document.getElementById(
            "windChart"
        );

    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    const items = getChartData(data);

    const labels = items.map(
        item =>
            formatChartTime(
                getValue(item, [
                    "timestamp",
                    "time",
                    "date"
                ])
            )
    );

    const values = items.map(
        item =>
            getValue(item, [
                "wind_speed",
                "wind_speed_10m",
                "wind"
            ])
    );

    destroyChart(windChart);

    windChart = new Chart(
        canvas,
        {
            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {
                        label: "Wind Speed (km/h)",

                        data: values,

                        tension: 0.35,

                        pointRadius: 2,

                        pointHoverRadius: 5
                    }

                ]

            },

            options: {

                ...getCommonOptions(),

                scales: {

                    x: {
                        grid: {
                            display: false
                        }
                    },

                    y: {

                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "km/h"
                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   Update All Charts
========================================================= */

function updateWeatherCharts(data) {

    createTemperatureChart(data);

    createRainChart(data);

    createHumidityChart(data);

    createWindChart(data);

}