from dotenv import load_dotenv
import os 
import base64
from requests import post, get
import json 


load_dotenv()

#Setting up the environment file to connect to spotify API
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Retrieving authentication token from spotify
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token" 
    headers = {
        "Authorization" : "Basic " + auth_base64, 
        "Content-type" : "application/x-www-form-urlencoded"
    }
    data = { "grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


### This function is used to send headers when wanting to lookup artist, songs, playlist when sending information to the API
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

### This is the function that is used to search for an artist and bring up the most popular result  
def search_for_artist(token, artist_name): 
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    ## If there was no result for the artist name reply that to the user
    if len(json_result) == 0:
        print("No results were found for this artist name")
        return None
    
    return json_result


token = get_token()
result = search_for_artist(token, "ACDC")

