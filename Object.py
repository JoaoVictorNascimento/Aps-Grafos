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
        return self.__dict__.keys()

    def json(self):
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

    def simplify(self):
        pass

    def factory(type, dictionary):
        if type == 'Track':
            return Track(dictionary)
        elif type == 'Playlist':
            return Playlist(dictionary)

        assert 0, "Falha ao criar objeto: " + type

    factory = staticmethod(factory)


class SimpleObject:
    def __init__(self):
        pass

    def __setitem__(self, key, value):
        super().__setattr__(key, value)

    def __getitem__(self, item):
        return super().__getattribute__(item)

    def add(self, key, value):
        self[key] = value

    def keys(self):
        return self.__dict__.keys()

    def json(self):
        return self.__dict__

    def print(self):
        for i in self.keys():
            print(i + ': ', self[i])
        print("----------")

    def __str__(self):
        return 'Music: ' + self['name']


class Playlist(ToObject):
    def simplify(self):
        playlist = SimpleObject()
        names = ['id', 'name', 'collaborative']
        for i in names:
            playlist.add(i, self[i])

        owner = ['id', 'display_name']
        for j in owner:
            playlist.add('owner' + "_" + j, self['owner'][j])
        return playlist

    def print(self, hash=''):
        self.simplify().print()


class Track(ToObject):

    def simplify(self):
        track = SimpleObject()

        names = ['id', 'name', 'popularity']
        for i in names:
            track.add(i, self[i])

        album = ['id', 'name']
        for j in album:
            track.add('album' + "_" + j, self['album'][j])
        # print(self['artists'][0].keys())

        artists = []
        for k in range(len(self['artists'])):
            artists.append({'id': self['artists'][k]['id'],
                            'name': self['artists'][k]['name']})

        track.add('artists', artists)

        artists = []
        for k in range(len(self['album']['artists'])):
            artists.append({'id': self['album']['artists'][k]['id'],
                            'name': self['album']['artists'][k]['name']})

        track.add('album' + "_" + 'artists', artists)

        return track

    def print(self, hash=''):
        self.simplify().print()
