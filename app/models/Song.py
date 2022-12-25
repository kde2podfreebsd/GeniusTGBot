import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from .Actor import Actor

class Song(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    name = conn.Column(conn.String(2048), nullable=False)
    text = conn.Column(conn.Text, nullable=True)
    actor_id = conn.Column(conn.Integer, conn.ForeignKey('actor.id'), nullable=False)
    actor = conn.relationship('Actor', backref=conn.backref('song', lazy=True))

    def __repr__(self):
        return '<Song %r>' % self.name

    def create(self, actor_name, name: str, text: str):
        """
        create question
        """

        with app.app_context():
            if Song.query.filter_by(name=name).first():
                return {"status": False, "msg": "Song already exist"}
            else:
                self.name = name
                self.text = text

                actor = Actor.query.filter_by(actor=actor_name).first()

                if actor:

                    actor.song.append(self)
                    current_db_sessions = conn.object_session(actor)
                    current_db_sessions.add(actor)
                    current_db_sessions.commit()

                    return {"status": True, "msg": "Song created"}

                return {"status": False, "msg": "Song not found"}
