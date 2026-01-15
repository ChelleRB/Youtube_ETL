import requests
import json

import os #needed for dotenv file which has the API key
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env") #load the .env file

API_KEY = os.getenv("API_KEY") #this gets the api key
CHANNEL_HANDLE = "ComedyBites"

def get_playlist_id():

  try:

    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
    response = requests.get(url)

    response.raise_for_status()

    data = response.json() 

    #print(json.dumps(data, indent=4))

    channel_items = data["items"][0]
    channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

    print(channel_playlistId)

    return channel_playlistId
  
  except requests.exceptions.RequestException as e:
    raise e
  
if __name__ == "__main__":
  #print("get playlist_id will be executed")
  get_playlist_id()
