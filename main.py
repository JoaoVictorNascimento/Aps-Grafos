import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import json
import time
from math import log
from functools import reduce
from Object import *
from Grafo import Graph


def main():
    graph = SpotList()


    var = graph.relation()
 
class SpotList:
    Client_ID = 'c1ba30fe3be544b9beaf1ddff027a0b7'
    Client_Secret = 'f471043ef395448ebcbab4c18a231980'

    def __init__(self):
        self.token = SpotifyClientCredentials(client_id=self.Client_ID,
                                              client_secret=self.Client_Secret)

        self.mygraph = Graph()
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

    def get_artist(self, art):
        artist = art
        items = artist[self.type]['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    # Album
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

    # Track
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
        track = list(map(lambda x: ToObject.factory('Track', x), reduce(lambda a, b: a + b, tracks)))

        return track

    def playlist(self):
        tracks = self.artist_top_tracks()

        music = []
        for i in tracks:
            for j in self.search(search=ToObject(i)['name'], q='', limit=3, type='playlist')['playlists']['items']:
                music.append(ToObject.factory(type='Playlist', dictionary=j).simplify())

        return music

    def contain_list(self,playlist, music_A, music_B):
        flagA = False
        flagB = False
        
        if(music_A['name'] == music_B['name']):
            return False

        for i in playlist:
            try:
                val = i['name'].index(music_A['name'])
                
                if val >= 0 :
                    flagA = True
            except ValueError:
                 pass

            try:
                val1 = i['name'].index(music_B['name'])
                if val1 >= 0 :
                    flagB = True
            except ValueError:
                 pass
        
        if (flagA == flagB) == True :
            return True
        
        else:
            return False

    


    def relation(self):
        playlist = self.playlist()
        playlists = []
        music = self.artist_top_tracks()

        for i in playlist:
            playlists.append(self.spotify.user_playlist(user=i['owner_id'], playlist_id=i['id']))

        test = []
        # print(playlist)
        playlist_music_name = []
        for i in playlists:
            for j in i['tracks']['items']:
                test.append(ToObject.factory('Track', j['track']))

            playlist_music_name.append(test)
            test = []

        arest = 0

        for music_a in music:
            for music_b in music:
                for playlist_music in playlist_music_name:
                    if self.contain_list(playlist_music,music_a,music_b) :
                        arest += 1

                if arest > len(playlist_music_name)*(0.98+(log(len(playlist_music_name),60)/100)):
                    self.mygraph.addNode(music_a['name'])
                    self.mygraph.addNode(music_b['name'])
                    self.mygraph.addEdge(music_a['name'],music_b['name'], arest)

                arest = 0
        
        self.mygraph.display()
        # print(self.mygraph.getEdges())

        return arest

       

    # Utils
    def print(self, objet=None, type=None):
        data = objet[type]
        # print(data.keys())
        for x in data['items']:
            print("-------------")
            # albums
            for i in x.keys():
                print(i, x[i])

    def load(self):
        return list(self.result[self.type]['items'])

    def keys(self):
        return self.result[self.type]['items'][0].keys()

    def __str__(self):
        return len(self.result)


if __name__ == "__main__":
    main()
