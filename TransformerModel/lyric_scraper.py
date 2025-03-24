import requests # web stuff
import csv
import re # regex
from bs4 import BeautifulSoup # web scraping

import os
from dotenv import load_dotenv # for loading environment variables from a.env file

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API token from environment variables
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")  # It fetches the API key from the .env file

def search_songs(artist: str="Taylor Swift"):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    search_url = f"{base_url}/search"
    params = {"q": artist}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in API response.")
        return None
    
def get_lyrics(song_url):
    response = requests.get(song_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics_div = soup.find('div', class_='lyrics')
    if lyrics_div:
        return lyrics_div.get_text()
    else:
        print("Couldn't find lyrics")
        return None
    
if __name__ == "__main__":
    scraped = search_songs()
