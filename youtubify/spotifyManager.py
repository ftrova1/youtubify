
def get_tracks_from_playlists(username, sp):
    playlists = sp.user_playlists(username)
    trackList = []
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print ('Parsing playlist : ',playlist['name'], 'by',playlist['owner']['display_name'],'\nNumber of tracks: ',playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],fields="tracks,next")
            tracks = results['tracks']
            for i, item in enumerate(tracks['items']):
                track = item['track']
                trackList.append(dict(id=track['id'],title=track['name'],
                                        artist=track['artists'][0]['name'],
                                        fulltitle=track['artists'][0]['name'] + ' - ' + track['name'],
                                        duration_ms = track['duration_ms']))

    return trackList
