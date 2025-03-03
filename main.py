from utils.update_pptx import *
from utils.get_datetime import get_sunday_text
from utils.crawl import *

prs = load_template("template/template__hansin4.pptx")


# 추가된 슬라이드 수 (페이지 수 재계산을 위해 사용)
cumulative_added_slide_count = 0

# 0. 표지 수정
next_sunday = get_sunday_text()
new_prs = edit_text_field(
  prs=prs,
  slide_index=0,
  is_title=True,
  new_text=next_sunday)

# 1. 기도자, 봉헌자, 광고, 성경봉독범위, 설교자, 결단찬양명, 축도자명 수정
NAME_OF_PRAYER = "김희수"
NAME_OF_OFFERING = "이현"
NAME_OF_ADS = "노진수"
BIBLE_RANGE = "요한복음 1:1-3"
TITLE_OF_SERMON = "설교 제목"
ENDING_SONG_TITLE = "결단찬양제목"
ENDING_PRAYER = "노진수"

new_prs = edit_text_field(
  prs=new_prs,
  slide_index=13,
  is_title=True,
  new_text=f"{NAME_OF_PRAYER} 청년",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=14,
  is_title=True,
  new_text=f"{NAME_OF_OFFERING} 청년",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=17,
  is_title=True,
  new_text=f"{NAME_OF_ADS} 목사",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=20,
  is_title=True,
  new_text=f"{BIBLE_RANGE}",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=22,
  is_title=True,
  new_text=f"{TITLE_OF_SERMON}",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=23,
  is_title=True,
  new_text=f"{ENDING_SONG_TITLE}",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=33,
  is_title=True,
  new_text=f"{ENDING_PRAYER} 목사",
  align_center=False
)

# 2. 찬양 파트 수정
songs = [
  {
    "title_page_index": 5,
    "lyrics_page_index": 6,
    "url": "https://music.bugs.co.kr/track/2578051",
    "title": "제목 1",
    "splitted_lyrics": [] 
  },
  {
    "title_page_index": 7,
    "lyrics_page_index": 8,
    "url": "https://music.bugs.co.kr/track/2578051",
    "title": "제목 2",
    "splitted_lyrics": [] 
  },
  {
    "title_page_index": 9,
    "lyrics_page_index": 10,
    "url": "https://music.bugs.co.kr/track/2578051",
    "title": "제목 3",
    "splitted_lyrics": [] 
  },
  {
    "title_page_index": 11,
    "lyrics_page_index": 12,
    "url": "https://music.bugs.co.kr/track/2578051",
    "title": "제목 4",
    "splitted_lyrics": [] 
  },
]

current_prs = new_prs

# Crawling
for index, song in enumerate(songs):
    crawled_data = crawl_lyrics(song["url"])
    songs[index]["splitted_lyrics"] = split_lyrics(crawled_text=crawled_data,json_url=f"utils/json/lyrics_song{index+1}.json")


# Make PPT
for index, song in enumerate(songs):
    title = song["title"]
    splited_lyrics = song["splitted_lyrics"]

    song_title_page_index = song["title_page_index"] + cumulative_added_slide_count
    song_lyrics_page_index = song["lyrics_page_index"] + cumulative_added_slide_count

    # Title 페이지 수정
    current_prs = edit_text_field(
      prs=current_prs,
      slide_index=song_title_page_index,
      is_title=True,
      new_text=title
    )

    # 가사 페이지 수정
    added_slide_res = duplicate_and_add_slide(
      prs= current_prs,
      duplicate_slide_index=song_lyrics_page_index,
      slide_texts=splited_lyrics
    )
    current_prs = added_slide_res["prs"]
    added_lyrics_slide_count = added_slide_res["added_slide_count"]
    cumulative_added_slide_count += added_lyrics_slide_count

new_prs = current_prs


# 3. 광고 페이지 추가
ads = [
  {
    "title": "# 광고 1",
    "contents": "광고 테스트\n광고 테스트\n광고 테스트"
  },
  {
    "title": "# 광고 2",
    "contents": "광고 테스트\n광고 테스트\n광고 테스트"
  }
]

page_of_ads = 19 + cumulative_added_slide_count
added_page_count_ads = add_ads_slides(new_prs, ads, page_of_ads)
cumulative_added_slide_count += (len(ads) - 1)

# 4. 성경봉독 슬라이드 추가
bible_contents = [
    {"title": "요한복음 1:1", "contents": "요한복음 1:1 내용"},
    {"title": "요한복음 1:2", "contents": "요한복음 1:2 내용"},
]

page_of_bible = 21 + cumulative_added_slide_count
add_bible_slides(new_prs, bible_contents, page_of_bible)
cumulative_added_slide_count += (len(bible_contents) - 1)


# 5. 결단 찬양 수정
ending_song = {
  "title_page_index": 23,
  "lyrics_page_index": 24,
  "url": "https://music.bugs.co.kr/track/2578051",
  "title": "결단 찬양 제목",
  "splitted_lyrics": [] 
}
ending_song_crawled_data = crawl_lyrics(ending_song["url"])
ending_song["splitted_lyrics"] = split_lyrics(crawled_text=ending_song_crawled_data, json_url="utils/json/lyrics_ending_song.json")

ending_song_title = ending_song["title"]
ending_song_splited_lyrics = ending_song["splitted_lyrics"]

ending_song_title_page_index = ending_song["title_page_index"] + cumulative_added_slide_count
ending_song_lyrics_page_index = ending_song["lyrics_page_index"] + cumulative_added_slide_count

# Title 페이지 수정
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=ending_song_title_page_index,
  is_title=True,
  new_text=ending_song_title,
  align_center=False
)

# 가사 페이지 수정
added_slide_res = duplicate_and_add_slide(
  prs= new_prs,
  duplicate_slide_index=ending_song_lyrics_page_index,
  slide_texts=ending_song_splited_lyrics
)
added_lyrics_slide_count = added_slide_res["added_slide_count"]
cumulative_added_slide_count += added_lyrics_slide_count

new_prs = added_slide_res["prs"]


# 프레젠테이션 저장
save_presentation(new_prs, "res/test.pptx")