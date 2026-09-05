/* =================================
   WeatherGPT Map
================================= */

let weatherMap = null;

let weatherMarker = null;


/* =================================
   Initialize Map
================================= */

function initializeWeatherMap(
    latitude,
    longitude,
    weather = null
) {

    const mapElement =
        document.getElementById(
            "weatherMap"
        ) ||
        document.getElementById(
            "dashboardMap"
        );


    if (!mapElement) {
        return;
    }


    if (
        latitude === undefined ||
        longitude === undefined
    ) {

        return;

    }


    if (typeof L === "undefined") {

        console.error(
            "Leaflet is not loaded."
        );

        return;

    }


    /* ------------------------------
       Create Map
    ------------------------------ */

    if (!weatherMap) {

        weatherMap =
            L.map(
                mapElement
            ).setView(
                [
                    latitude,
                    longitude
                ],
                10
            );


        L.tileLayer(

            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

            {

                attribution:
                    "&copy; OpenStreetMap contributors"

            }

        ).addTo(
            weatherMap
        );

    } else {

        weatherMap.setView(
            [
                latitude,
                longitude
            ],
            10
        );

    }


    /* ------------------------------
       Marker
    ------------------------------ */

    if (weatherMarker) {

        weatherMap.removeLayer(
            weatherMarker
        );

    }


    weatherMarker =
        L.marker(
            [
                latitude,
                longitude
            ]
        ).addTo(
            weatherMap
        );


    let popup =
        "Selected Location";


    if (weather) {

        popup = `

            <strong>
                ${weather.location || "Location"}
            </strong>

            <br>

            Temperature:
            ${weather.temperature ?? "--"}°C

            <br>

            Condition:
            ${weather.condition || "--"}

        `;

    }


    weatherMarker.bindPopup(
        popup
    );


    weatherMarker.openPopup();


    /* ------------------------------
       Update Map Information
    ------------------------------ */

    updateMapInformation(
        weather,
        latitude,
        longitude
    );

}


/* =================================
   Update Map Info
================================= */

function updateMapInformation(
    weather,
    latitude,
    longitude
) {

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
        "mapLocation",
        weather?.location || "--"
    );


    setText(
        "mapCoordinates",
        `${latitude}, ${longitude}`
    );


    setText(
        "mapTemperature",
        weather?.temperature !== undefined
            ? `${weather.temperature}°C`
            : "--°C"
    );


    setText(
        "mapCondition",
        weather?.condition || "--"
    );

}


/* =================================
   Map Page Search
================================= */

async function initializeMapPage() {

    const input =
        document.getElementById(
            "mapLocationInput"
        );

    const button =
        document.getElementById(
            "mapSearchButton"
        );


    if (!input || !button) {
        return;
    }


    const saved =
        getSavedLocation();


    if (saved) {

        try {

            const weather =
                await fetchCurrentWeather(
                    saved
                );


            initializeWeatherMap(
                weather.latitude,
                weather.longitude,
                weather
            );

        } catch (error) {

            console.error(
                error
            );

        }

    }


    button.addEventListener(
        "click",
        async () => {

            const errorElement =
                document.getElementById(
                    "mapError"
                );


            clearError(
                errorElement
            );


            try {

                const weather =
                    await searchLocation(
                        input.value
                    );


                saveLocation({

                    location:
                        weather.location,

                    latitude:
                        weather.latitude,

                    longitude:
                        weather.longitude

                });


                initializeWeatherMap(
                    weather.latitude,
                    weather.longitude,
                    weather
                );


            } catch (error) {

                showError(
                    errorElement,
                    error.message
                );

            }

        }
    );

}


/* =================================
   Map Page Initialization
================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (
            document.getElementById(
                "weatherMap"
            )
        ) {

            initializeMapPage();

        }

    }
);