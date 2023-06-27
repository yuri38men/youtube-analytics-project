import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.channel_description = self.channel['items'][0]['snippet']['description']
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        with open('moscowpython.json', 'w') as outfile:
            json.dump({'channel_id': self.__channel_id, 'channel': self.channel, 'title': self.title,
                       'channel_description': self.channel_description, 'url': self.url,
                       'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                       'view_count': self.view_count}, outfile)
