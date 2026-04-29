# event_event_models_final

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'

    # -------------------------
    # PRIMARY KEY
    # -------------------------
    id = db.Column(db.Integer, primary_key=True)

    # -------------------------
    # ONLY FIELD REQUIRED
    # -------------------------
    name = db.Column(db.String(100), nullable=False)

    # -------------------------
    # TIMESTAMP
    # -------------------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -------------------------
    # CONVERT TO JSON
    # -------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }