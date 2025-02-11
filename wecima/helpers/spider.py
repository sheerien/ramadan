# import re
# from typing import List, Optional
# from httpx_html import HTMLSession
# from httpx import RequestError
# from selectolax.parser import HTMLParser

# class WeCimaScraper:
#     """
#     A utility class for scraping WeCima, including methods to extract MP4 URLs,
#     fetch pagination details, and extract series and episode data.
#     """

#     def __init__(self):
#         """
#         Initializes the WeCimaScraper with an HTMLSession.
#         """
#         self.session = HTMLSession()

#     def extract_mp4s(self, text: str) -> Optional[List[str]]:
#         """
#         Extract MP4 URLs from the provided text.

#         Args:
#             text (str): The input text to search for MP4 URLs.

#         Returns:
#             Optional[List[str]]: A list of MP4 URLs, or None if no URLs are found.
#         """
#         try:
#             pattern = r"https?://.*?\.mp4"  # Regex pattern for MP4 URLs
#             mp4_urls = re.findall(pattern, text)
#             return mp4_urls if mp4_urls else None
#         except Exception as e:
#             print(f"Error extracting MP4 URLs: {e}")
#             return None

#     def get_pagination(self, total_pages: int, base_url: str) -> List[str]:
#         """
#         Generates a list of paginated URLs for the series list.

#         Args:
#             total_pages (int): The total number of pagination pages.
#             base_url (str): The base URL to generate the paginated URLs.

#         Returns:
#             List[str]: A list of URLs for each page in the pagination.

#         Raises:
#             ValueError: If total_pages is not a valid positive integer.
#             TypeError: If total_pages is not an integer.
#         """
#         try:
#             pages = []  # List to store pagination URLs
            
#             # Ensure total_pages is an integer
#             if not isinstance(total_pages, int):
#                 raise TypeError(f"total_pages must be an integer, but got {type(total_pages)}")

#             # Ensure the total number of pages is a positive integer
#             if total_pages < 1:
#                 raise ValueError("total_pages must be a positive integer.")

#             # Generate pagination URLs based on the total number of pages
#             for i in range(1, total_pages + 1):
#                 pages.append(f"{base_url}{i}")

#             return pages  # Return the list of generated URLs

#         except TypeError as e:
#             print(f"Error: {e}")
#             return []
#         except ValueError as e:
#             print(f"Error: {e}")
#             return []



# scraper = WeCimaScraper()


import re
from typing import List, Optional, Dict
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser

class WeCimaScraper:
    """
    A utility class for scraping WeCima, including methods to extract MP4 URLs,
    fetch pagination details, and extract series and episode data.
    """
    
    def __init__(self):
        """
        Initializes the WeCimaScraper with an HTMLSession.
        """
        self.session = HTMLSession()
    
    def extract_mp4s(self, text: str) -> Optional[List[str]]:
        """
        Extract MP4 URLs from the provided text.

        Args:
            text (str): The input text to search for MP4 URLs.

        Returns:
            Optional[List[str]]: A list of MP4 URLs, or None if no URLs are found.
        """
        try:
            pattern = r"https?://.*?\\.mp4"  # Regex pattern for MP4 URLs
            mp4_urls = re.findall(pattern, text)
            return mp4_urls if mp4_urls else None
        except Exception as e:
            print(f"Error extracting MP4 URLs: {e}")
            return None
    
    def get_pagination(self, total_pages: int, base_url: str) -> List[str]:
        """
        Generates a list of paginated URLs for the series list.

        Args:
            total_pages (int): The total number of pagination pages.
            base_url (str): The base URL to generate the paginated URLs.

        Returns:
            List[str]: A list of URLs for each page in the pagination.
        """
        try:
            # Validate that total_pages is a positive integer
            if not isinstance(total_pages, int) or total_pages < 1:
                raise ValueError("total_pages must be a positive integer.")

            # Generate pagination URLs
            return [f"{base_url}{i}" for i in range(1, total_pages + 1)]
        
        except ValueError as e:
            print(f"Error: {e}")
            return []

    # def get_series_list_urls(self, pages: List[str], headers: Dict[str, str]) -> List[Dict[str, str]]:
    #     """
    #     Extracts a list of series from the given paginated URLs.
        
    #     Args:
    #         pages (List[str]): A list of paginated URLs.
    #         headers (Dict[str, str]): Headers for the HTTP request.
        
    #     Returns:
    #         List[Dict[str, str]]: A list of dictionaries containing series ID, title, and URL.
    #     """
    #     series_list = []
    #     count = 0
        
    #     try:
    #         for page in pages:
    #             response = self.session.get(url=page, headers=headers)
    #             response.raise_for_status()  # Raise error for non-200 responses
                
    #             html = response.html.html
    #             parser = HTMLParser(html)
    #             main_grid = parser.css_first("div.Grid--WecimaPosts")
                
    #             if not main_grid:
    #                 print(f"Warning: No grid found on {page}")
    #                 continue
                
    #             grid_items = main_grid.css("div.GridItem")
                
    #             for item in grid_items:
    #                 count += 1
    #                 title = item.css_first("a").attributes.get("title", "Unknown").strip()
    #                 url = item.css_first("a").attributes.get("href", "#").strip()
    #                 series_list.append({"id": count, "title": title, "url": url})
            
    #         return series_list if series_list else []
        
    #     except RequestError as e:
    #         print(f"HTTP request error: {e}")
    #         return []
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")
    #         return []


    def get_series_list_urls(self, pages: List[str], headers: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Extracts a list of series from the given paginated URLs, ensuring uniqueness.
        
        Args:
            pages (List[str]): A list of paginated URLs.
            headers (Dict[str, str]): Headers for the HTTP request.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries containing series ID, title, and URL.
        """
        series_list = []
        seen_titles = set()  # لتتبع المسلسلات الفريدة
        count = 0
        
        try:
            for page in pages:
                response = self.session.get(url=page, headers=headers)
                response.raise_for_status()  # التأكد من أن الرد ناجح
                
                html = response.html.html
                parser = HTMLParser(html)
                main_grid = parser.css_first("div.Grid--WecimaPosts")
                
                if not main_grid:
                    print(f"Warning: No grid found on {page}")
                    continue
                
                grid_items = main_grid.css("div.GridItem")
                
                for item in grid_items:
                    title = item.css_first("a").attributes.get("title", "Unknown").strip()
                    url = item.css_first("a").attributes.get("href", "#").strip()
                    
                    if title not in seen_titles:  # التحقق من التكرار
                        seen_titles.add(title)
                        count += 1
                        series_list.append({"id": count, "title": title, "url": url})
            
            return series_list if series_list else []
        
        except RequestError as e:
            print(f"HTTP request error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

# Example usage
scraper = WeCimaScraper()
