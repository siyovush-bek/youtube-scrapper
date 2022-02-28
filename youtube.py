from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.parse as p
import os
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()

def video_length(text):
    text = text.replace('PT', '')
    text = text.replace('H', ':')
    text = text.replace('M', ':')
    text = text.replace('S', '')
    return text

def search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()

def extract_data(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    response = get_video_details(youtube, id=video_id)
    items = response.get("items")[0]
    # get the snippet, statistics & content details from the video response
    snippet         = items["snippet"]
    statistics      = items["statistics"]
    content_details = items["contentDetails"]
    # get infos from the snippet
    result = {
        'Title of the Video': snippet["title"],
        'Video Link': url,
        'Number of Comments': statistics.get("commentCount", 'xx'),
        'Total Likes': statistics.get("likeCount", 0),
        'Total Views': statistics["viewCount"],
        'Channel Name': snippet["channelTitle"],
        'Name of Speaker': 'xx',
    }

    duration = content_details["duration"]
    # duration in the form of something like 'PT5H50M15S'
    # parsing it to be something like '5:50:15'
    # Azim salom aytayapti Hindistonga!
    # parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
    duration_str = video_length(duration)

    result.update({
        'Video Length': duration_str,
        'Words Per min': 'xx',
        'Average Length of Sentence': 'xx',
        'Word repetition': 'xx',
        'Filler Words': 'xx',
        'Volume': 'xx',
        'Type': 'xx',
        # 'Duration': duration,
    })

    return result
