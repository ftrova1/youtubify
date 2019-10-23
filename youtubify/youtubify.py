from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import config
import argparse

client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID, client_secret=config.SPOTIPY_CLIENT_SECRET)

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

def main (username):
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = get_tracks_from_playlists(username, sp)
    # results = sp.user_playlists(username)
    print (json.dumps(results, indent=4))

if __name__ == '__main__':
    print ('Starting...')
    parser = argparse.ArgumentParser(description='This sript will grab user playlists')
    parser.add_argument('--username', help='username')
    args = parser.parse_args()
    main(args.username)

# results = results['tracks']['items']
