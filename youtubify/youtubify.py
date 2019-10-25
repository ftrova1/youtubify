from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import config
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
from spotifyManager import get_tracks_from_playlists
from youtubeManager import addVideoToPlaylist,findVideosBySongTitle,getMyYoutubePlaylists,retrieveFirstVideo

client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID, client_secret=config.SPOTIPY_CLIENT_SECRET)
api_service_name = 'youtube'
api_version = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
client_config = {
    'installed': {
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token',
        'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob'],
        'client_id': config.YOUTUBE_CLIENT_ID,
        'client_secret': config.YOUTUBE_CLIENT_SECRET
    }
}

def main (username):
    #Instantiating Spotipy...
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #Instantiating YT...
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_console()
    youtube = build(api_service_name, api_version, credentials=credentials)

    #Getting spotify trackList
    results = get_tracks_from_playlists(username, sp)
    print (json.dumps(results, indent=4))
    ####################################
    ####################################
    ids = findVideosBySongTitle(youtube, 'Salmo')
    retrieveFirstVideo(youtube,ids)

if __name__ == '__main__':
    print ('Starting...')
    parser = argparse.ArgumentParser(description='This script will retrieve the tracks you want from your Spotify playlists and add them into your favourite Youtube playlist')
    parser.add_argument('--username', help='username')
    args = parser.parse_args()
    main(args.username)
