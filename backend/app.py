from flask import Flask, jsonify
from flask_cors import CORS

from backend.config.config import Config

from backend.routes.weather_routes import weather_bp
from backend.routes.forecast_routes import forecast_bp
from backend.routes.map_routes import map_bp
from backend.routes.alert_routes import alert_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    # Register routes
    app.register_blueprint(weather_bp)
    app.register_blueprint(forecast_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(alert_bp)


    @app.route("/api/health", methods=["GET"])
    def health():

        return jsonify({

            "success": True,

            "status": "ok",

            "service": "WeatherGPT Backend"

        })


    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )