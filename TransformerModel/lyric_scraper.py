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
    print(response.text)
    lyrics_div = soup.find('div', class_='lyrics')
    if lyrics_div:
        return lyrics_div.get_text()
    else:
        print("Couldn't find lyrics")
        return None
    
def fetch_all_lyrics(artist):
    song_data = search_songs(artist)
    if not song_data: return []
    songs = song_data["response"]["hits"]
    all_lyrics = []
    for song in songs:
        song_url = song["result"]["url"]
        lyrics = get_lyrics(song_url)
        if lyrics:
            title = song_data['title']
            all_lyrics.append({"title": title, "lyrics": lyrics})
            print(f"Fetched lyrics for: {title}")
    
    return all_lyrics

def clean_lyrics(text):
    text = text.lower()
    text = re.sub(r"\[.*?\]", "", text)  # Remove section labels
    text = re.sub(r"[^\w\s']", "", text)  # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    return text

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "lyrics"])
        writer.writeheader()
        for song in data:
            writer.writerow(song)


if __name__ == "__main__":
    artist = "Taylor Swift"
    lyrics_data = fetch_all_lyrics(artist)

    # Clean the lyrics and prepare data for CSV
    cleaned_data = []
    for song in lyrics_data:
        cleaned_data.append({
            "title": song["title"],
            "lyrics": clean_lyrics(song["lyrics"])
        })

    # Save the cleaned data to a CSV file
    save_to_csv(cleaned_data, "taylor_swift_lyrics.csv")
    print("Lyrics saved to taylor_swift_lyrics.csv.")
