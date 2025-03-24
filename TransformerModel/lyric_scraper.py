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

def get_lyrics(song_url):
    """Scrape song lyrics from a Genius song URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(song_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {song_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # Find the lyrics container (Genius uses a div with 'data-lyrics-container' attribute)
    lyrics_divs = soup.find_all("div", {"data-lyrics-container": "true"})
    if not lyrics_divs:
        print(f"Lyrics not found for {song_url}")
        return None
    # Extract text from all found divs
    lyrics = "\n".join([div.get_text(separator="\n") for div in lyrics_divs])
    return lyrics.strip()

music_dir = "../TrainingSongs"
music_files = glob.glob(f"{music_dir}/**/*.*", recursive=True)
valid_extensions = {"mp3"}
music_files = [file for file in music_files if any(file.lower().endswith(ext) for ext in valid_extensions)]
song_names = sorted([os.path.splitext(os.path.basename(file))[0] for file in music_files])
song_urls = [generate_song_url("Taylor Swift", song_title) for song_title in song_names]

lyrics_spam = [get_lyrics(url) for url in song_urls]
lyrics_spam = { song_names[i] : lyrics for i, lyrics in enumerate(lyrics_spam)}

with open("taylor_swift_lyrics.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Song", "Lyrics"])
    for song, lyrics in lyrics_spam.items():
        writer.writerow([song, lyrics])
    print(f"Lyrics saved!")
    csvfile.close()