import requests
from bs4 import BeautifulSoup
import json

def crawl_lyrics(song_url: str) -> str:
    response = requests.get(song_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics: str = soup.select_one('div.lyricsContainer xmp').get_text()
    print("crawled lyrics finished: \n", lyrics)
    return lyrics

def split_lyrics(crawled_text: str, json_url: str) -> list:
    # LLM API를 연동하기 전입니다.
    with open(json_url, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["lyrics"]
    return []

def get_bible_contents(bible_book: str, begin_ch: int, begin_verse: int, end_ch: int, end_verse: int) -> list:
    get_bible_url = f"https://ibibles.net/quote.php?kor-{bible_book}/{begin_ch}:{begin_verse}-{end_ch}:{end_verse}"
    # https://ibibles.net/quote.php?kor-mat/5:3-12
    response = requests.get(get_bible_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    verses = []
    for small_tag in soup.find_all('small'):
        verse_number = small_tag.text
        verse_content = small_tag.next_sibling.strip()
        verses.append({"title": f"마태복음 {verse_number}", "contents": verse_content})

    return verses