import requests
import json

import os #needed for dotenv file which has the API key
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env") #load the .env file

API_KEY = os.getenv("API_KEY") #this gets the api key
CHANNEL_HANDLE = "ComedyBites"
maxResults = 50
#playlist = UUGfUuxBzB8E30XjCjOvji2w

def get_playlist_id():

  try:

    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
    response = requests.get(url)

    response.raise_for_status()

    data = response.json() 

    #print(json.dumps(data, indent=4))

    channel_items = data["items"][0]
    channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

    print(channel_playlistId) #after I ran the pipeline I got the playlistId printed = UUGfUuxBzB8E30XjCjOvji2w

    return channel_playlistId
  
  except requests.exceptions.RequestException as e:
    raise e
  

def get_video_ids(playlistId):

  video_ids = [] #intilized empty list first to store video ids of the channel

  pageToken = None

  base_url= f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}" 

  try:

    while True:
      url = base_url

      if pageToken:
        url += f"&pageToken={pageToken}" #the url will update each time with the page token to get the next set of results

      response = requests.get(url)

      response.raise_for_status()

      data = response.json() #if theres no error, we get the json response-goes thru content details to get video id value

      for item in data.get("items", []): #loop through the items in the response and extract the video id from each item and append it to the video_ids list
        video_id = item["contentDetails"]["videoId"]
        video_ids.append(video_id)

      pageToken = data.get("nextPageToken") #get the next page token to continue fetching results

      if not pageToken: #if there is no next page token, we have fetched all the video ids and can break out of the loop
        break
    
    return video_ids

  except requests.exceptions.RequestException as e:
      raise e


if __name__ == "__main__":
  #print("get playlist_id will be executed")
  playlistId = get_playlist_id()
  videoId = get_video_ids(playlistId) #to test remember to use print

# STEP 1 playlist ID(channels) 
# STEP 2 goes to.. VIDEO ID(playlistId items) 
# STEP 3 goes to VIDEO DATA (videos)
