import requests # web stuff
import csv
import re # regex
from bs4 import BeautifulSoup # web scraping

GENIUS_CLIENT_ID = "3QDIwshW18t8pJfqOBaFLGVnRFjJYy6ha7Uwt1hD4CzPmWLeF2XDIix6nfawjet9"
GENIUS_CLIENT_SECRET = "0liJ0RxGqls0qZjNGDH8PDZ9aiM8pL3T_wbe99tdzK-O9lZjsdw_5nRHQQJP1fq0Rsv1FvFNKm3JxaIejQApjA"
GENIUS_API_TOKEN = "NlUyo-mjbksV45dGf6mppJ987fqhZqfaVxWJCYwCzlG628wH2raWzx7DhYHlNGWR"

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
    
if __name__ == "__main__":
    scraped = search_songs()
    print(scraped)