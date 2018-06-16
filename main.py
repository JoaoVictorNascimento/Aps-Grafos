import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import json
import spotipy
import time
from functools import reduce

def main():
    graph = Graph()
    #val = graph.artist()
    #print(val[1]['id'])
    val = graph.artist_top_tracks()
    print(val)
    # test = []
    # for i in val:
    #     # print (i.keys())
    #     test.append(i['tracks'])
    # z = reduce(lambda a,b: a+b, test)


    
    # exemplo busca por cantor
    #val = graph.search(search="Metallica", q='',type='artist')
    #print(val['artists']['items'][0].print())
    
    #graph.print(graph.result,'artists')
    #asd = ToObject(graph.get_artist(graph.result))
    #asd.print()
    
    # print(graph.result)
    # carregar album
    #graph.show_artist_albums()

    #graph.artist_top_tracks()
    #graph.print()

class ToObject:
    def __init__(self, dictionary):
        if isinstance(dictionary, str) or not dictionary:
            pass
        else:
            if not isinstance(dictionary, str):
                for i in dictionary.keys():
                    if isinstance(dictionary[i], dict):
                        self.add(i, dictionary[i])
                    elif isinstance(dictionary[i], list):
                        self.addlist(i, dictionary[i])
                    else:
                        self[i] = dictionary[i]

    def __setitem__(self, key, value):
        super().__setattr__(key, value)

    def __getitem__(self, item):
        return super().__getattribute__(item)

    def add(self, key, value):
        self[key] = ToObject(value)

    def keys(self):
        return self.__dict__

    def addlist(self, key, value):
        list = []
        for i in value:
            list.append(ToObject(i))
        self[key] = list

    def print(self, hash=''):
        for i in self.__dict__:
            if isinstance(self[i], list):
                print(i, ':')
                for j in self[i]:
                    j.print(hash + '-')
            if isinstance(self[i], ToObject):
                print(i, ':')
                self[i].print(hash + '-')
            else:
                print(hash, i, ':', self[i])

class Graph:
    Client_ID = 'c1ba30fe3be544b9beaf1ddff027a0b7'
    Client_Secret = 'f471043ef395448ebcbab4c18a231980'

    def __init__(self):
        self.token = SpotifyClientCredentials(client_id=self.Client_ID,
                                              client_secret=self.Client_Secret)

        self.type = ''
        self.spotify = spotipy.Spotify(client_credentials_manager=self.token)
        self.result = []
    
    def search(self, q='', type='track', search=None):
        self.type = type + 's'
        objsearch = self.spotify.search(q=q + search, type=type)
        return ToObject(objsearch)

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
        listartist = []
        
        for i in art:
            artist = self.search(search=i, q='', type='artist')
            listartist.append(self.get_artist(artist))
        
        return listartist
    


    def __str__(self):
        return len(self.result)
    
    


if __name__ == "__main__":
    main()
