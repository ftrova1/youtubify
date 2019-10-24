import config
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build

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

def getMyYoutubePlaylists(youtube):
    request = youtube.playlists().list(part = 'id', mine = True)
    response = request.execute()
    print (json.dumps(response, indent=4))

def addVideoToPlaylist(youtube,videoID,playlistID):
      add_video_request=youtube.playlistItem().insert(
      part="snippet",
      body={
            'snippet': {
              'playlistId': playlistID,
              'resourceId': {
                      'kind': 'youtube#video',
                  'videoId': videoID
                }
            #'position': 0
            }
    }
     ).execute()

def findVideosBySongTitle(youtube, songTitle):
    videoIds = []
    request = youtube.search().list(q=songTitle, type='video', part='id', maxResults=2)
    videos = request.execute()
    for vid in videos['items']:
        videoIds.append(vid['id']['videoId'])
    return videoIds

def retrieveFirstVideo(youtube, videoIds):
    id = videoIds[0]
    request = youtube.videos().list(id=id, part='snippet,contentDetails')
    videos = request.execute()
    print(videos['items'][0]['snippet']['title'])


def main():
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_console()
    youtube = build(api_service_name, api_version, credentials=credentials)
    ids = findVideosBySongTitle(youtube, 'Salmo')
    retrieveFirstVideo(youtube,ids)

if __name__ == '__main__':
    print('Starting YTmanager...')
    main()
