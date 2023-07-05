import os
import datetime

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='snippet, contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        best_video = None
        most_likes = 0
        for video in video_response['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > most_likes:
                most_likes = likes
                best_video = video

        link = None
        if best_video:
            link = f'https://youtu.be/{best_video["id"]}'
        return link
