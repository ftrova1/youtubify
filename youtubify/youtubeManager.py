import config
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build

api_service_name = 'youtube'
api_version = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
client_config = {
    'installed': {
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token',
        'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob'],
        'client_id': config.YOUTUBE_CLIENT_ID,
        'client_secret': config.YOUTUBE_CLIENT_SECRET
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
credentials = flow.run_console()

youtube = build(api_service_name, api_version, credentials=credentials)

request = youtube.playlists().list(part = 'snippet', mine = True)
response = request.execute()

print (json.dumps(response, indent=4))
