import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.link_to_video = "https://www.youtube.com/channel/" + self.video_id
        self.number_of_views = self.video_response['items'][0]['statistics']['viewCount']
        self.number_of_likes = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.video_response['items'][0]['snippet']['title']

    def __str__(self):
        return f"{self.playlist_videos}"
