from utils.llm import *
from utils.update_pptx import *
from utils.get_datetime import get_sunday_text
from utils.crawl import *
import json
from datetime import datetime

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
print("Completed: 표지 수정", next_sunday)

# 1. 기도자, 봉헌자, 광고, 성경봉독범위, 설교자, 결단찬양명, 축도자명 수정
## 1-1. Requirements LLM Execution & JSON import
req_text = ""
with open("prompts/user_input/req_text_paster.txt", "r", encoding="utf-8") as file:
    req_text = file.read()
req_paster_json_path = make_requirements_of_paster_json(req_text)

req_paster_json_path = "utils/json/res_requirements_paster.json"
requirements_paster = {}
with open(req_paster_json_path, "r", encoding="utf-8") as file:
    requirements_paster = json.load(file)
print("Completed: Make requirements of paster json")


## 1-2. PPT 슬라이드
SLIDE_INDEX_PRAYER = 13
SLIDE_INDEX_OFFERING = 14
SLIDE_INDEX_ADS = 17
SLIDE_INDEX_BIBLE_RANGE = 20
SLIDE_INDEX_SERMON_TITLE = 22
SLIDE_INDEX_ENDING_SONG_TITLE = 23
SLIDE_INDEX_ENDING_PRAYER = 33

NAME_OF_PRAYER = requirements_paster["NAME_OF_PRAYER"]
NAME_OF_OFFERING = requirements_paster["NAME_OF_OFFERING"]
NAME_OF_ADS = requirements_paster["NAME_OF_ADS"]

bible_range_obj = requirements_paster["BIBLE_RANGE"]
BIBLE_RANGE = f'{bible_range_obj["BIBLE_BOOK"]} {bible_range_obj["BIBLE_CH_BEGIN"]}:{bible_range_obj["BIBLE_VERSE_BEGIN"]} - {bible_range_obj["BIBLE_CH_END"]}:{bible_range_obj["BIBLE_VERSE_END"]}' 
TITLE_OF_SERMON = requirements_paster["TITLE_OF_SERMON"]
ENDING_SONG_TITLE = requirements_paster["ENDING_SONG_TITLE"]
ENDING_PRAYER = requirements_paster["ENDING_PRAYER"]

new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_PRAYER,
  is_title=True,
  new_text=NAME_OF_PRAYER,
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_OFFERING,
  is_title=True,
  new_text=NAME_OF_OFFERING,
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_ADS,
  is_title=True,
  new_text=NAME_OF_ADS,
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_BIBLE_RANGE,
  is_title=True,
  new_text=BIBLE_RANGE,
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_SERMON_TITLE,
  is_title=True,
  new_text=TITLE_OF_SERMON,
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_ENDING_SONG_TITLE,
  is_title=True,
  new_text=f"{ENDING_SONG_TITLE}",
  align_center=False
)
new_prs = edit_text_field(
  prs=new_prs,
  slide_index=SLIDE_INDEX_ENDING_PRAYER,
  is_title=True,
  new_text=ENDING_PRAYER,
  align_center=False
)
print("Completed: 기도자, 봉헌자, 광고, 성경봉독범위, 설교자, 결단찬양명, 축도자명 수정")

# 2. 찬양 파트 수정
# current_prs = new_prs
# SLIDE_INDEX_START_SONG = 5

# ## 2-1. 크롤링 수행
# after_crawled = []
# req_team_wakeup_txt = ""
# with open("prompts/user_input/req_text_teamwakeup.txt", "r", encoding="utf-8") as file:
#   req_team_wakeup_txt = file.read()
# organized_req_wakeup_json_path = organize_requirements_of_team_wakeup(requirements_txt=req_team_wakeup_txt)

# with open(organized_req_wakeup_json_path, "r", encoding="utf-8") as file:
#     requirements = json.load(file)
#     for requirement in requirements:
#         crawled_data = crawl_lyrics(requirement["url"])
#         after_crawled.append({
#           "title": requirement["title"],
#           "lyrics": crawled_data
#         })
# print("Completed: Crawling Songs (Team Wakeup)")

# ## 2-2. LLM을 활용한 split 수행
# splitted_lyrics = []
# splited_lyrics_json_path = 'utils/json/requirements_team_wakeup_splited.json'
# split_lyrics_to_json(crawled_text_list=after_crawled, json_path=splited_lyrics_json_path)

# splited_lyrics_json_path = "utils/json/requirements_team_wakeup_splited.json"
# with open(splited_lyrics_json_path, "r", encoding="utf-8") as file:
#     splitted_lyrics = json.load(file) # [{"title": "제목", "splitted_lyrics": ["첫 번째 슬라이드 가사", "두 번째 슬라이드 가사"]}, ...]
# print("Completed: Split Lyrics (Team Wakeup)")


# songs = []
# for index, splitted_lyric in enumerate(splitted_lyrics):
#     songs.append({
#       "title_page_index": SLIDE_INDEX_START_SONG + index * 2,
#       "lyrics_page_index": SLIDE_INDEX_START_SONG + 1 + index * 2,
#       "title": splitted_lyric["title"],
#       "splitted_lyrics": splitted_lyric["splitted_lyrics"]
#     })
# print("Completed: Organize Songs (Team Wakeup)")

# # songs = [
# #   {
# #     "title_page_index": 5,
# #     "lyrics_page_index": 6,
# #     "url": "https://music.bugs.co.kr/track/2578051",
# #     "title": "제목 1",
# #     "splitted_lyrics": [] 
# #   },
# #   {
# #     "title_page_index": 7,
# #     "lyrics_page_index": 8,
# #     "url": "https://music.bugs.co.kr/track/2578051",
# #     "title": "제목 2",
# #     "splitted_lyrics": [] 
# #   },
# #   {
# #     "title_page_index": 9,
# #     "lyrics_page_index": 10,
# #     "url": "https://music.bugs.co.kr/track/2578051",
# #     "title": "제목 3",
# #     "splitted_lyrics": [] 
# #   },
# #   {
# #     "title_page_index": 11,
# #     "lyrics_page_index": 12,
# #     "url": "https://music.bugs.co.kr/track/2578051",
# #     "title": "제목 4",
# #     "splitted_lyrics": [] 
# #   },
# # ]

# # Crawling
# # for index, song in enumerate(songs):
# #     crawled_data = crawl_lyrics(song["url"])
# #     songs[index]["splitted_lyrics"] = split_lyrics(crawled_text=crawled_data,json_url=f"utils/json/lyrics_song{index+1}.json")


# # 2-3. PPT 슬라이드 생성
# for index, song in enumerate(songs):
#     title = song["title"]
#     splited_lyrics = song["splitted_lyrics"]

#     song_title_page_index = song["title_page_index"] + cumulative_added_slide_count
#     song_lyrics_page_index = song["lyrics_page_index"] + cumulative_added_slide_count

#     # Title 페이지 수정
#     current_prs = edit_text_field(
#       prs=current_prs,
#       slide_index=song_title_page_index,
#       is_title=True,
#       new_text=title
#     ) 

#     # 가사 페이지 수정
#     added_slide_res = duplicate_and_add_slide(
#       prs= current_prs,
#       duplicate_slide_index=song_lyrics_page_index,
#       slide_texts=splited_lyrics
#     )
#     current_prs = added_slide_res["prs"]
#     added_lyrics_slide_count = added_slide_res["added_slide_count"]
#     cumulative_added_slide_count += added_lyrics_slide_count

# new_prs = current_prs
# print("Completed: 찬양 파트 PPT 추가")

# 3. 광고 페이지 추가
ads = requirements_paster["ads"]
SLIDE_INDEX_ADS_CONTENTS = 19
# ads = [
#   {
#     "title": "# 광고 1",
#     "contents": "광고 테스트\n광고 테스트\n광고 테스트"
#   },
#   {
#     "title": "# 광고 2",
#     "contents": "광고 테스트\n광고 테스트\n광고 테스트"
#   }
# ]

page_of_ads = SLIDE_INDEX_ADS_CONTENTS + cumulative_added_slide_count
added_page_count_ads = add_ads_slides(new_prs, ads, page_of_ads)
cumulative_added_slide_count += (len(ads) - 1)
print("Completed: 광고 페이지 추가")

# 4. 성경봉독 슬라이드 추가
bible_range_obj = requirements_paster["BIBLE_RANGE"]
bible_contents = get_bible_contents(bible_book=bible_range_obj["BIBLE_BOOK"], begin_ch=bible_range_obj["BIBLE_CH_BEGIN"], begin_verse=bible_range_obj["BIBLE_VERSE_BEGIN"], end_ch=bible_range_obj["BIBLE_CH_END"], end_verse=bible_range_obj["BIBLE_VERSE_END"])
SLIDE_INDEX_BIBLE_CONTENTS = 21

# bible_contents = [
#     {"title": "요한복음 1:1", "contents": "요한복음 1:1 내용"},
#     {"title": "요한복음 1:2", "contents": "요한복음 1:2 내용"},
# ]

page_of_bible = SLIDE_INDEX_BIBLE_CONTENTS + cumulative_added_slide_count
add_bible_slides(new_prs, bible_contents, page_of_bible)
cumulative_added_slide_count += (len(bible_contents) - 1)
print("Completed: 성경 말씀 슬라이드 추가")


# 5. 결단 찬양 수정
ending_song = requirements_paster["ending_song"]
# ending_song = {
#   "title_page_index": 23,
#   "lyrics_page_index": 24,
#   "url": "https://music.bugs.co.kr/track/2578051",
#   "title": "결단 찬양 제목",
#   "splitted_lyrics": []
# }

ending_song_crawled_text = crawl_lyrics(ending_song["url"])
ending_song_crawled_data = [ending_song_crawled_text]
split_lyrics_to_json(crawled_text_list=ending_song_crawled_data, json_path="utils/json/lyrics_ending_song.json")

with open("utils/json/lyrics_ending_song.json", "r", encoding="utf-8") as file:
    ending_song["splitted_lyrics"] = json.load(file)

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
print("Completed: 결단 찬양 추가")


# 프레젠테이션 저장 (path: res/날짜_청년한신_4부예배.pptx)
from datetime import datetime
today = datetime.today().strftime('%y%m%d')
save_file_path = f"res/{today}_청년한신_4부예배.pptx"
save_presentation(new_prs, save_file_path)
print("Completed: All Process")
print("Saved: ", save_file_path)