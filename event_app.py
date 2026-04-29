# event_event_app_py_final_real_fixed

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from event_models import db


def create_app():
    load_dotenv()

    # 👉 ensure static folder is used (where demo.html lives)
    app = Flask(__name__, static_folder="static")
    CORS(app)

    # 👉 DB config (relative file in project folder)
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


if __name__ == '__main__':
    app = create_app()

    port = 5001

    # 👉 get local network IP (for QR testing on phones)
    local_ip = "127.0.0.1"
    try:
        import socket
        local_ip = socket.gethostbyname(socket.gethostname())
    except:
        pass

    print(f"\nServer running:")
    print(f"Local:   http://127.0.0.1:{port}")
    print(f"Network: http://{local_ip}:{port}\n")

    port = int(os.environ.get("PORT", 5001))
app.run(host='0.0.0.0', port=port)