import requests # web stuff
import csv
import re # regex
from bs4 import BeautifulSoup # web scraping

import os
from dotenv import load_dotenv # for loading environment variables from a.env file
import glob

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API token from environment variables
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")  # It fetches the API key from the .env file

def generate_song_url(artist, song_title):
    """Generate a Genius URL based on artist and song title, handling special formats."""
    artist = artist.lower().replace(" ", "-")  # Convert spaces to dashes
    song_title = song_title.lower()
    song_title = re.sub(r"[^\w\s']", "", song_title)
    song_title = song_title.replace(" ", "-").replace("(", "").replace(")", "").replace("'", "")
    song_url = f"https://genius.com/{artist}-{song_title}-lyrics"
    return song_url

music_dir = "../TrainingSongs"
music_files = glob.glob(f"{music_dir}/**/*.*", recursive=True)
valid_extensions = {"mp3"}
music_files = [file for file in music_files if any(file.lower().endswith(ext) for ext in valid_extensions)]
song_names = [os.path.splitext(os.path.basename(file))[0] for file in music_files]

for song in song_names:
    print(song)

song_urls = [generate_song_url()]