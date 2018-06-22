from SpotfyAPIConnector import Connector


if __name__ == "__main__":
    Client_ID = 'c1ba30fe3be544b9beaf1ddff027a0b7'
    Client_Secret = 'f471043ef395448ebcbab4c18a231980'

    # Init API
    spot = Connector(Client_ID, Client_Secret)

    # Search Track
    track = None
    for i in spot.track(search="CPM22", limit=10):
        # print(i.keys())
        track = i.simplify()
        track.print()
        # print(track)


    # # Search Music in N Playlist
    # for i in spot.playlist(search=track.name, limit=10):
    #     playlist = i.simplify()
    #     playlist.print()
