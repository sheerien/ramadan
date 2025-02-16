# local imports
from wecima.helpers import OUTPUT_DIR, WECIMA_OUTPUT_DIR, DB_PATH, scraper, save_to_json, read_data_from_json_file, download_video
from wecima.Settings import settings, headers
#libs imports
import re
from typing import List, Optional
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser
from dataclasses import dataclass

session = HTMLSession()


pages = scraper.get_pagination(total_pages=settings.WECIMA_PAGINATION, base_url=settings.WECIMA_SITE_Series_List_URL)

series_list = scraper.get_series_list_urls(pages=pages, headers=headers)


for series in series_list:
    print()
    print(series)


save_to_json(series_list, f"{WECIMA_OUTPUT_DIR}series_list.json")

@dataclass
class Series:
    id: int
    title: str
    url: str

data = read_data_from_json_file(f"{WECIMA_OUTPUT_DIR}series_list.json")



series_list: List[Series] = [Series(**item) for item in data]


series_data = []

for i, series in enumerate(series_list):
    print(series.id)
    print(series.title)
    print(series.url)
    eps = scraper.get_episodes_list(url=series.url, headers=headers)
    series_data.append({"id":int(i+1), "series_name": series.title, "series_count": len(eps), "eps": eps})


for series_d in series_data:
    print()
    print(series_d)

save_to_json(series_data, f"{WECIMA_OUTPUT_DIR}episodes_from_series_list.json")


# This code snippet is performing the following tasks:
@dataclass
class SeriesObj:
    id: int
    series_name: str
    series_count: int
    eps: List[str]



data = read_data_from_json_file(f"{WECIMA_OUTPUT_DIR}episodes_from_series_list.json")

series_objects = [SeriesObj(**item) for item in data]


mp4_data = []
# print(series_list_data)
for obj in series_objects:
    print()
    print(obj.series_count)
    print(obj.series_name)
    if len(obj.eps) !=0:
        print(obj.eps[-1])
        mp4s = scraper.get_mp4s(url=obj.eps[-1], headers=headers)
        print(obj.series_count)
        print(obj.series_name)
        if len(mp4s) !=0:
            print(mp4s[0])
            mp4_data.append({"season": 1, "count":obj.series_count, "name":obj.series_name, "mp4":mp4s[0]})

for mp4 in mp4_data:
    print()
    print(mp4)


save_to_json(mp4_data, f"{WECIMA_OUTPUT_DIR}mp4.json")

@dataclass
class Episode:
    season: int
    count: int
    name: str
    mp4: str

data = read_data_from_json_file(f"{WECIMA_OUTPUT_DIR}mp4.json")

eps: List[Episode] = [Episode(**episode) for episode in data]

for ep in eps:
    print()
    print(ep.name)
    print()
    download_video(url=ep.mp4, series_name=ep.name, output_folder="series_mp4s", referer=settings.WECIMA_SITE_URL, season=ep.season, episode=ep.count)




# Example usage
# url = r"https://varcdnx9-16.bom1bom.online:82/d/n5rwveilbgeyf3tk54pjb7kmnsorkgrl4eaze6irwiyegcojvb46zbanlxvft5oe2jrxwstu/Bnat.Lhded.E28.weciima.autos.mp4"
# series_name = "Hood_Al_Layl"
# download_video(url=url, series_name=series_name, referer=settings.WECIMA_SITE_URL, season=2, episode=10)

