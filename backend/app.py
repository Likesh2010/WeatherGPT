from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from backend.config.config import Config

from backend.routes.weather_routes import weather_bp
from backend.routes.forecast_routes import forecast_bp
from backend.routes.map_routes import map_bp
from backend.routes.alert_routes import alert_bp


# Frontend directory
FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

CORS(app)


# Register API routes
app.register_blueprint(weather_bp)
app.register_blueprint(forecast_bp)
app.register_blueprint(map_bp)
app.register_blueprint(alert_bp)


# -----------------------------
# Frontend routes
# -----------------------------

@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/dashboard")
def dashboard():
    return send_from_directory(
        FRONTEND_DIR,
        "dashboard.html"
    )


@app.route("/map")
def map_page():
    return send_from_directory(
        FRONTEND_DIR,
        "map.html"
    )


# -----------------------------
# Health check
# -----------------------------

@app.route("/api/health")
def health_check():
    return jsonify({
        "success": True,
        "message": "WeatherGPT backend is running"
    })


# -----------------------------
# Error handlers
# -----------------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": {
            "code": "NOT_FOUND",
            "message": "The requested resource was not found."
        }
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred."
        }
    }), 500


if __name__ == "__main__":
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )