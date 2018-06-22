import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import json
import spotipy
import time
from functools import reduce
from Object import *

def main():
    graph = Graph()
    #val = graph.artist()
    #print(val[1]['id'])
    val = graph.playlist()

    #print(val)
    for i in val:
        playlist = i.simplify()
        print(playlist)
   
    
    #      test.append(i['tracks'])
    # z = reduce(lambda a,b: a+b, test)


    
    # exemplo busca por cantor
    
    # val = graph.search(search="Alok", q='', limit=20, type='playlist')
    #var2 = val['playlists']['items'] 
   
    #for i in var2:
    #    print(i['name'])
    
    #      test.append(i['tracks'])
    # z = reduce(lambda a,b: a+b, test)

    #graph.print(graph.result,'artists')
    #asd = ToObject(graph.get_artist(graph.result))
    #asd.print()
    
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
    
    # Search
    def search(self, q='', type='track', search=None, limit=10):
        self.type = type + 's'
        objsearch = self.spotify.search(q=q + search, type=type, limit=limit)
        return ToObject(objsearch)

    # Artist
    def artist(self):
        art = sys.argv[1:]
        listartist = []
        
        for i in art:
            artist = self.search(search=i, q='', type='artist')
            listartist.append(self.get_artist(artist))
        
        return listartist

    def get_artist(self,art):
        artist = art
        items = artist[self.type]['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    #Album
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

    
    #Track
    # retorna uma lista com as 10 musicas mais populares de cada artista
    def artist_top_tracks(self):
        # self.results = top_tracks(self.get_artist()['id'])
        artists = self.artist()
        top_tracks = []
        tracks = []
        for i in artists:
            top_tracks.append(ToObject(self.spotify.artist_top_tracks(i['id']))) 
    
        for i in top_tracks:
            tracks.append(i['tracks'])
        
        track = reduce(lambda a,b: a+b, tracks)

        return track
    
    def playlist(self):
        tracks = self.artist_top_tracks()
        
        music = []
        for i in tracks:
            for j in self.search(search=ToObject(i)['name'], q='', limit=3, type='playlist')['playlists']['items']:
                music.append(ToObject.factory(type='Playlist', dictionary=j))

        return music

    
         


    #Utils
    def print(self, objet=None, type=None):
        data = objet[type]
        # print(data.keys())
        for x in data['items']:
            print("-------------")
            # albums
            for i in x.keys():
                print(i,x[i])
    
    
    def load(self):
        return list(self.result[self.type]['items'])

    def keys(self):
        return self.result[self.type]['items'][0].keys()
    


    def __str__(self):
        return len(self.result)
    
    


if __name__ == "__main__":
    main()
