from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from Object import *


class Connector:
    # search(q, limit=10, offset=0, type='track', market=None)

    def __init__(self, Client_ID, Client_Secret):
        self.token = SpotifyClientCredentials(client_id=Client_ID, client_secret=Client_Secret)

    def track(self, search, limit=1):
        spotify = spotipy.Spotify(client_credentials_manager=self.token)

        music = []

        for i in spotify.search(q=search, limit=limit, type='track', market=None)['tracks']['items']:
            music.append(ToObject.factory(type='Track', dictionary=i))

        return music

    def playlist(self, search, limit=1):
        spotify = spotipy.Spotify(client_credentials_manager=self.token)

        music = []

        for i in spotify.search(q=search, limit=limit, type='playlist', market=None)['playlists']['items']:
            music.append(ToObject.factory(type='Playlist', dictionary=i))

        return music
