import os
import lyricsgenius
from dotenv import load_dotenv
from typing import Optional

config = load_dotenv()
token = os.getenv("geniusapikey")
genius = lyricsgenius.Genius(token)

class GeniusAPI:
    __instance = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GeniusAPI, cls).__new__(cls)
        return cls.instance


    def get_lyrics(self, artist: str, songname: str):
        artist = genius.search_artist(artist, max_songs=1, sort="title")
        song = artist.song(songname)
        return str(song.lyrics)


    def get_artist_description(self, artist: str):
        artist = genius.search_artist(artist, max_songs=1, sort="title")
        return str(artist._body['description']['plain'])





