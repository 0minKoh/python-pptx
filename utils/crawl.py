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

# def split_lyrics() -> list:
#     # LLM API를 연동하기 전입니다.
#     input("json 파일이 준비되면 아무 키나 누르세요")
#     with open("utils/json/lyrics.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
#         return data["lyrics"]
#     return []