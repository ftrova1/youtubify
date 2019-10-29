from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import config
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
from spotifyManager import get_tracks_from_playlists
from youtubeManager import addVideosToPlaylist,findVideosBySongTitle,getMyYoutubePlaylists,retrieveFirstVideo

client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID, client_secret=config.SPOTIPY_CLIENT_SECRET)
api_service_name = 'youtube'
api_version = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
client_config = {
    'installed': {
        'prompt' : 'consent',
        'access_type' : 'offline',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token',
        'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob'],
        'client_id': config.YOUTUBE_CLIENT_ID,
        'client_secret': config.YOUTUBE_CLIENT_SECRET
    }
}

def main (username, playlist):
    #Instantiating Spotipy...
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #Instantiating YT...
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_console()
    youtube = build(api_service_name, api_version, credentials=credentials)

    #Getting spotify trackList
    titles = []
    spotifySongs = get_tracks_from_playlists(username, sp)
    for song in spotifySongs:
        titles.append(song['fulltitle'])
    #print (json.dumps(spotifySongs, indent=4))
    videos = []
    for title in titles:
        id = findVideosBySongTitle(youtube, title , 1)
        videos.append(dict(title=title, id = id ))
    #print(videos)
    addVideosToPlaylist(youtube,videos,playlist)
    #     print('Elementi aggiunti.')
    # else :
    #     print('Qualcosa è andato storto...')

if __name__ == '__main__':
    print ('Starting...')
    parser = argparse.ArgumentParser(description='This script will retrieve the tracks you want from your Spotify playlists and add them into your favourite Youtube playlist')
    parser.add_argument('--username', required = True, help='Spotify ID')
    parser.add_argument('--playlist', required = True, help='Youtube playlist ID')
    args = parser.parse_args()
    main(args.username, args.playlist)
