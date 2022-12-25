import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from typing import Optional


class Actor(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    actor = conn.Column(conn.Text, nullable=False)
    description = conn.Column(conn.Text, nullable=True)

    def __repr__(self):
        return '<Actor %r>' % self.actor

    def create(self, actor: str, description: Optional[str] = None):
        """
        create question
        """

        with app.app_context():
            if Actor.query.filter_by(actor=actor).first():
                return {"status": False, "msg": "Actor already exist"}
            else:

                self.actor = actor
                self.description = description if description is not None else None

                conn.session.add(self)
                conn.session.commit()

                return {"status": True, "msg": "Actor created"}