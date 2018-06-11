import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys


def main():
    graph = Graph()

    # exemplo busca por cantor
    graph.search(search="Evanescence")

    # carregar album
    graph.show_artist_albums()


class Graph:
    Client_ID = 'c1ba30fe3be544b9beaf1ddff027a0b7'
    Client_Secret = 'f471043ef395448ebcbab4c18a231980'

    def __init__(self):
        self.token = SpotifyClientCredentials(client_id=self.Client_ID,
                                              client_secret=self.Client_Secret)

        self.type = ''
        self.spotify = spotipy.Spotify(client_credentials_manager=self.token)
        self.result = []

    def search(self, q='artist:', type='artist', search=None):
        self.type = type + 's'
        self.result = self.spotify.search(q=q + search, type=type)

    def get_artist(self):
        results = self.result
        items = results[self.type]['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    def show_artist_albums(self):
        albums = []
        results = self.spotify.artist_albums(self.get_artist()['id'], album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.spotify.next(results)
            albums.extend(results['items'])
        seen = set()  # to avoid dups
        albums.sort(key=lambda album: album['name'].lower())
        for album in albums:
            name = album['name']
            if name not in seen:
                print((' ' + name))
                seen.add(name)

    def load(self):
        return list(self.result[self.type]['items'])

    def keys(self):
        return self.result[self.type]['items'][0].keys()

    def print(self):
        for x in self.load():
            print("-------------")
            for i in self.keys():
                print("\t - " + i + ":", x[i])

    def __str__(self):
        return len(self.result)


if __name__ == "__main__":
    main()
