/* =================================
   Weather Alerts
================================= */


async function fetchAlerts(location) {

    const params =
        new URLSearchParams();


    if (location.latitude !== undefined) {

        params.append(
            "latitude",
            location.latitude
        );

    }


    if (location.longitude !== undefined) {

        params.append(
            "longitude",
            location.longitude
        );

    }


    const response =
        await fetch(
            `${API_BASE_URL}/weather/alerts?${params.toString()}`
        );


    if (!response.ok) {

        throw new Error(
            "Unable to retrieve alerts."
        );

    }


    const result =
        await response.json();


    if (!result.success) {

        throw new Error(
            result.error?.message ||
            "Alert data unavailable."
        );

    }


    return result.data;

}


/* =================================
   Render Alerts
================================= */

function renderAlerts(data) {

    const container =
        document.getElementById(
            "alertsContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    const alerts =
        data.alerts ||
        data ||
        [];


    if (!Array.isArray(alerts) ||
        alerts.length === 0) {

        container.innerHTML = `

            <div class="no-alerts">
                ✅ No active weather alerts.
            </div>

        `;

        return;

    }


    alerts.forEach(
        alert => {

            const severity =
                (
                    alert.severity ||
                    "moderate"
                ).toLowerCase();


            const element =
                document.createElement(
                    "div"
                );


            element.className =
                `alert alert-${severity}`;


            element.innerHTML = `

                <strong>
                    ${alert.type || "Weather Alert"}
                </strong>

                <p>
                    ${alert.message || alert.description || ""}
                </p>

                ${
                    alert.recommendation
                        ? `
                            <small>
                                Recommendation:
                                ${alert.recommendation}
                            </small>
                        `
                        : ""
                }

            `;


            container.appendChild(
                element
            );

        }
    );

}


/* =================================
   Load Alerts
================================= */

async function loadAlerts(
    location
) {

    try {

        const data =
            await fetchAlerts(
                location
            );


        renderAlerts(
            data
        );

    } catch (error) {

        console.error(
            "Alert error:",
            error
        );

    }

}


/* =================================
   Risk Analysis
================================= */

async function loadRiskAnalysis(
    weather
) {

    if (!weather) {
        return;
    }


    /*
       The backend should eventually return
       calculated risk information.

       For now, the frontend safely displays
       whatever risk data the backend provides.
    */


    const risk =
        weather.risk ||
        null;


    if (!risk) {
        return;
    }


    updateRiskCard(
        "overallRisk",
        risk.overall
    );


    updateRiskCard(
        "heatRisk",
        risk.heat
    );


    updateRiskCard(
        "rainRisk",
        risk.rain
    );


    updateRiskCard(
        "windRisk",
        risk.wind
    );


    updateRiskCard(
        "floodRisk",
        risk.flood
    );

}


/* =================================
   Update Risk Card
================================= */

function updateRiskCard(
    elementId,
    risk
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element || !risk) {
        return;
    }


    const level =
        typeof risk === "string"
            ? risk
            : risk.level;


    if (!level) {
        return;
    }


    element.textContent =
        level.toUpperCase();


    element.className =
        "";


    element.classList.add(
        "risk-badge"
    );


    element.classList.add(
        `risk-${level.toLowerCase()}`
    );

}