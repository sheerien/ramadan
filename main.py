# local imports
from wecima.helpers import OUTPUT_DIR, WECIMA_OUTPUT_DIR, DB_PATH, scraper, save_to_json
from wecima.Settings import settings, headers
#libs imports
import re
from typing import List, Optional
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser

session = HTMLSession()


pages = scraper.get_pagination(total_pages=settings.WECIMA_PAGINATION, base_url=settings.WECIMA_SITE_Series_List_URL)

series_list = scraper.get_series_list_urls(pages=pages, headers=headers)


for series in series_list:
    print()
    print(series)


save_to_json(series_list, f"{WECIMA_OUTPUT_DIR}series_list.json")