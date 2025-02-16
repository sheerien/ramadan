import logging
import re
from typing import List
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from wecima.helpers import (
    OUTPUT_DIR, WECIMA_OUTPUT_DIR, DB_PATH, scraper, 
    save_to_json, read_data_from_json_file, download_video
)
from wecima.Settings import settings, headers

# Configure logging
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("wecima_scraper.log")
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])

session = HTMLSession()

@dataclass
class Series:
    id: int
    title: str
    url: str

@dataclass
class SeriesObj:
    id: int
    series_name: str
    series_count: int
    eps: List[str]

@dataclass
class Episode:
    season: int
    count: int
    name: str
    mp4: str

def fetch_series_list() -> List[Series]:
    """Fetches the list of series from the website."""
    try:
        pages = scraper.get_pagination(total_pages=settings.WECIMA_PAGINATION, base_url=settings.WECIMA_SITE_Series_List_URL)
        series_list = scraper.get_series_list_urls(pages=pages, headers=headers)
        save_to_json(series_list, f"{WECIMA_OUTPUT_DIR}series_list.json")
        return [Series(**item) for item in series_list]
    except Exception as e:
        logging.error(f"Error fetching series list: {e}")
        return []

def fetch_episodes(series_list: List[Series]) -> List[SeriesObj]:
    """Fetches episode lists for each series."""
    series_data = []
    for i, series in enumerate(series_list):
        try:
            eps = scraper.get_episodes_list(url=series.url, headers=headers)
            series_data.append({
                "id": i + 1,
                "series_name": series.title,
                "series_count": len(eps),
                "eps": eps
            })
        except Exception as e:
            logging.error(f"Error fetching episodes for {series.title}: {e}")
    
    save_to_json(series_data, f"{WECIMA_OUTPUT_DIR}episodes_from_series_list.json")
    return [SeriesObj(**item) for item in series_data]

def fetch_mp4_links(series_objects: List[SeriesObj]) -> List[Episode]:
    """Fetches MP4 links for the last episode of each series."""
    mp4_data = []
    for obj in series_objects:
        if not obj.eps:
            continue
        
        try:
            mp4s = scraper.get_mp4s(url=obj.eps[-1], headers=headers)
            if mp4s:
                mp4_data.append({
                    "season": 1,
                    "count": obj.series_count,
                    "name": obj.series_name,
                    "mp4": mp4s[0]
                })
        except Exception as e:
            logging.error(f"Error fetching MP4 links for {obj.series_name}: {e}")
    
    save_to_json(mp4_data, f"{WECIMA_OUTPUT_DIR}mp4.json")
    return [Episode(**episode) for episode in mp4_data]

def download_episodes(eps: List[Episode]):
    """Downloads the episodes."""
    for ep in eps:
        try:
            download_video(
                url=ep.mp4, 
                series_name=ep.name, 
                # output_folder="series_mp4s", 
                referer=settings.WECIMA_SITE_URL, 
                season=ep.season, 
                episode=ep.count
            )
        except Exception as e:
            logging.error(f"Error downloading episode {ep.name} - S{ep.season}E{ep.count}: {e}")

def main():
    """Main function to run the scraper workflow."""
    logging.info("Starting Wecima scraper...")
    series_list = fetch_series_list()
    if not series_list:
        logging.error("No series found. Exiting.")
        return
    
    series_objects = fetch_episodes(series_list)
    if not series_objects:
        logging.error("No episode data found. Exiting.")
        return
    
    episodes = fetch_mp4_links(series_objects)
    if not episodes:
        logging.error("No MP4 links found. Exiting.")
        return
    
    download_episodes(episodes)
    logging.info("Wecima scraper finished successfully.")

if __name__ == "__main__":
    main()
