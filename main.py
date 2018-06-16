import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import json
import spotipy
import time

def main():
    graph = Graph()
    graph.artist()
    print(graph.artist())
    

    # exemplo busca por cantor
    #graph.search(search="Metallica", q='',type='artist')
    #graph.print(graph.result,'artists')
    #print(graph.get_artist(graph.result))
    
    # print(graph.result)
    # carregar album
    #graph.show_artist_albums()

    #graph.artist_top_tracks()
    #graph.print()


class Graph:
    Client_ID = 'c1ba30fe3be544b9beaf1ddff027a0b7'
    Client_Secret = 'f471043ef395448ebcbab4c18a231980'

    def __init__(self):
        self.token = SpotifyClientCredentials(client_id=self.Client_ID,
                                              client_secret=self.Client_Secret)

        self.type = ''
        self.spotify = spotipy.Spotify(client_credentials_manager=self.token)
        self.result = []
        self.listartist = []

    def search(self, q='artist:', type='artist', search=None):
        self.type = type + 's'
        self.result = self.spotify.search(q=q + search, type=type)

    def get_artist(self,art):
        artist = art
        items = artist[self.type]['items']
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
    
    def artist_top_tracks(self):
        tracks=[]
        # self.results = top_tracks(self.get_artist()['id'])
        self.print(self.spotify.artist_top_tracks(self.get_artist()['id']), 'tracks')
    
    def print(self, objet=None, type=None):
        data = objet[type]
        # print(data.keys())
        for x in data['items']:
            print("-------------")
            # albums
            for i in x.keys():
                print(i,x[i])
    
    def artist(self):
        art = sys.argv[1:]
        for i in art:
            artist = self.search(search=i)
        return art

    def __str__(self):
        return len(self.result)
    
    


if __name__ == "__main__":
    main()
