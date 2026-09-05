# WeatherGPT

WeatherGPT is an intelligent web-based weather analysis platform that goes beyond traditional weather applications.

It combines live weather information, forecasts, visual analytics, weather-risk analysis, maps, alerts, and machine learning to provide users with a better understanding of weather conditions.

---

## Features

- Live weather information
- Location-based weather search
- Current weather conditions
- Multi-day weather forecast
- Temperature, humidity, wind and precipitation information
- Weather risk analysis
- Heat risk detection
- Rain risk detection
- Wind risk detection
- Flood-related risk analysis
- Weather alerts
- Interactive weather map
- Data visualization using charts
- Machine learning-based risk prediction
- ML prediction confidence
- Responsive web interface

---

## Project Architecture

```text
User
 |
 v
Frontend
 |
 v
Flask Backend
 |
 +-------------------+
 |                   |
 v                   v
Weather API       Risk Analysis
 |                   |
 v                   v
Weather Data       ML Model
 |                   |
 +---------+---------+
           |
           v
       WeatherGPT
           |
           v
       Dashboard