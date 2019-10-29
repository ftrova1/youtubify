import config
import json


def getMyYoutubePlaylists(youtube):
    request = youtube.playlists().list(part = 'id', mine = True)
    response = request.execute()
    print (json.dumps(response, indent=4))

def addVideosToPlaylist(youtube,videos,playlistID):
    for video in videos:
        add_video_request=youtube.playlistItems().insert( part="snippet",
                                                      body={
                                                            'snippet': {
                                                              'playlistId': playlistID,
                                                              'resourceId': {
                                                                      'kind': 'youtube#video',
                                                                      'videoId': video['id']
                                                                }
                                                            }
                                                        }).execute()
                                                        print('Video added: ', video['title'], ' - ', video['id'] )

def findVideosBySongTitle(youtube, songTitle, n):
    request = youtube.search().list(q=songTitle, type='video', part='id', maxResults=n)
    videos = request.execute()
    if n > 1 :
        videoIds = []
        for vid in videos['items']:
            videoIds.append(vid['id']['videoId'])
        return videoIds
    else:
        return videos['items'][0]['id']['videoId']

def retrieveFirstVideo(youtube, videoIds):
    id = videoIds[0]
    request = youtube.videos().list(id=id, part='snippet,contentDetails')
    videos = request.execute()
    print(videos['items'][0]['snippet']['title'])
