from flask import request, jsonify, Blueprint
from config import app
from models import Actor, Song
from db import conn
from cli import bp
from geniusAPI import GeniusAPI
from flask_swagger_ui import get_swaggerui_blueprint
import os

print(app.root_path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "KURSACH"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.app_context().push()

app.config.from_pyfile("config.py")
app.config['JSON_AS_ASCII'] = False

conn.init_app(app)

app.register_blueprint(bp)

@app.route("/actor", methods=['POST'])
def actor_post():
    try:
        new_actor = Actor()

        gapi = GeniusAPI()
        description = gapi.get_artist_description(artist=request.json['actor'])

        output = new_actor.create(
            actor= request.json['actor'],
            description = description
        )

        return jsonify(output)

    except Exception as e:
        print(e)
        pass

@app.route("/actor/<actor_name>", methods=['GET'])
def actor_get(actor_name):
    try:
        if request.method == 'GET':
            actor = Actor.query.filter_by(actor=actor_name).first()
            if actor:
                return {
                    "actor": actor.actor,
                    "description": actor.description
                }

            return str(False)


    except Exception as e:
        print(e)
        pass


@app.route("/song", methods=['POST'])
def song_post():
    try:
        new_song = Song()

        gapi = GeniusAPI()

        text = gapi.get_lyrics(artist=request.json['actor_name'], songname=request.json['songname'])

        output = new_song.create(
            actor_name=request.json['actor_name'],
            name= request.json['songname'],
            text= text
        )
        return jsonify(output)

    except Exception as e:
        print(e)
        pass

@app.route("/song/<song_name>", methods=['GET'])
def song_get(song_name):
    try:
        if request.method == 'GET':
            song = Song.query.filter_by(name=song_name).first()
            if song:
                return {
                    "name": song.name,
                    "text": song.text
                }

            return str(False)


    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")