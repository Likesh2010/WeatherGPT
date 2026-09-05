/* =================================
   Weather Charts
================================= */

let temperatureChart = null;
let rainChart = null;
let humidityChart = null;
let windChart = null;


/* =================================
   Extract Hourly Data
================================= */

function getHourlyData(data) {

    return data.hourly ||
           data.forecast ||
           [];

}


/* =================================
   Destroy Existing Chart
================================= */

function destroyChart(chart) {

    if (chart) {

        chart.destroy();

    }

}


/* =================================
   Temperature Chart
================================= */

function createTemperatureChart(data) {

    const canvas =
        document.getElementById(
            "temperatureChart"
        );


    if (!canvas) {
        return;
    }


    const hourly =
        getHourlyData(data);


    const labels =
        hourly.map(
            item =>
                formatChartTime(
                    item.timestamp ||
                    item.date
                )
        );


    const values =
        hourly.map(
            item =>
                item.temperature ?? null
        );


    destroyChart(
        temperatureChart
    );


    temperatureChart =
        new Chart(
            canvas,
            {
                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {
                            label:
                                "Temperature (°C)",

                            data: values,

                            tension: 0.35,

                            fill: true
                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        y: {
                            beginAtZero: false
                        }

                    }

                }

            }
        );

}


/* =================================
   Rain Chart
================================= */

function createRainChart(data) {

    const canvas =
        document.getElementById(
            "rainChart"
        );


    if (!canvas) {
        return;
    }


    const hourly =
        getHourlyData(data);


    const labels =
        hourly.map(
            item =>
                formatChartTime(
                    item.timestamp ||
                    item.date
                )
        );


    const values =
        hourly.map(
            item =>
                item.precipitation ?? 0
        );


    destroyChart(
        rainChart
    );


    rainChart =
        new Chart(
            canvas,
            {
                type: "bar",

                data: {

                    labels: labels,

                    datasets: [

                        {
                            label:
                                "Precipitation (mm)",

                            data: values

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }
        );

}


/* =================================
   Humidity Chart
================================= */

function createHumidityChart(data) {

    const canvas =
        document.getElementById(
            "humidityChart"
        );


    if (!canvas) {
        return;
    }


    const hourly =
        getHourlyData(data);


    const labels =
        hourly.map(
            item =>
                formatChartTime(
                    item.timestamp ||
                    item.date
                )
        );


    const values =
        hourly.map(
            item =>
                item.humidity ?? null
        );


    destroyChart(
        humidityChart
    );


    humidityChart =
        new Chart(
            canvas,
            {
                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {
                            label:
                                "Humidity (%)",

                            data: values,

                            tension: 0.35
                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        y: {

                            min: 0,

                            max: 100

                        }

                    }

                }

            }
        );

}


/* =================================
   Wind Chart
================================= */

function createWindChart(data) {

    const canvas =
        document.getElementById(
            "windChart"
        );


    if (!canvas) {
        return;
    }


    const hourly =
        getHourlyData(data);


    const labels =
        hourly.map(
            item =>
                formatChartTime(
                    item.timestamp ||
                    item.date
                )
        );


    const values =
        hourly.map(
            item =>
                item.wind_speed ?? null
        );


    destroyChart(
        windChart
    );


    windChart =
        new Chart(
            canvas,
            {
                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {
                            label:
                                "Wind Speed (km/h)",

                            data: values,

                            tension: 0.35
                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }

        );

}


/* =================================
   Update All Charts
================================= */

function updateWeatherCharts(
    data
) {

    createTemperatureChart(data);

    createRainChart(data);

    createHumidityChart(data);

    createWindChart(data);

}


/* =================================
   Time Formatter
================================= */

function formatChartTime(value) {

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
            hour: "2-digit"
        }
    );

}