# event_event_app_py_final_render_ready

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from event_models import db


def create_app():
    load_dotenv()

    # 👉 Flask app with static folder (for demo.html)
    app = Flask(__name__, static_folder="static")
    CORS(app)

    # 👉 Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind DB
    db.init_app(app)

    # Import and register routes
    from event_routes import api_bp
    app.register_blueprint(api_bp)

    # -----------------------------
    # SERVE MINI WEBSITE (QR TARGET)
    # -----------------------------
    @app.route("/demo")
    def demo_page():
        return app.send_static_file("demo.html")

    # -----------------------------
    # HEALTH CHECK
    # -----------------------------
    @app.route("/")
    def home():
        return {"status": "Backend running"}

    # -----------------------------
    # CREATE TABLES
    # -----------------------------
    with app.app_context():
        db.create_all()

    return app


# 🔥 REQUIRED FOR GUNICORN (DO NOT REMOVE)
app = create_app()