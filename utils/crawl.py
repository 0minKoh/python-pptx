import requests
from bs4 import BeautifulSoup
from utils.data.bible_code import get_bible_code
import json
import os

from utils.llm import call_llm_api

def crawl_lyrics(song_url: str) -> str:
    response = requests.get(song_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics: str = soup.select_one('div.lyricsContainer xmp').get_text()
    print("crawled lyrics finished: \n", lyrics)
    return lyrics

def split_lyrics_to_json(req_split_lyrics: list) -> str:
    # 1. import prompt template: prompts/prompt_requirement_team_wakeup_2.txt
    prompt_req_lyrics_split = f"```json\n{req_split_lyrics}\n```\n\n"
    with open("prompts/prompt_requirement_team_wakeup_2.txt", "r", encoding="utf-8") as file:
        prompt_req_lyrics_split += file.read()

    # 2. call LLM API
    response = call_llm_api(prompt_req_lyrics_split)

    # 3. save response to 'utils/json/requirements_team_wakeup_splited.json'
    json_path = "utils/json/requirements_team_wakeup_splited.json"
    with open(json_path, "w", encoding="utf-8") as file:
        file.write(response)
    
    return json_path

def get_bible_contents(bible_book: str, begin_ch: int, begin_verse: int, end_ch: int, end_verse: int) -> list:
    bible_book_code = get_bible_code(bible_book)
    get_bible_url = f"https://ibibles.net/quote.php?kor-{bible_book_code}/{begin_ch}:{begin_verse}-{end_ch}:{end_verse}"
    # https://ibibles.net/quote.php?kor-mat/5:3-12
    response = requests.get(get_bible_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    verses = []
    for small_tag in soup.find_all('small'):
        verse_number = small_tag.text
        verse_content = small_tag.next_sibling.strip()
        verses.append({"title": f"마태복음 {verse_number}", "contents": verse_content})

    return verses