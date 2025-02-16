# import re
# from typing import List, Optional, Dict
# from httpx_html import HTMLSession
# from httpx import RequestError
# from selectolax.parser import HTMLParser

# class WeCimaScraper:
#     """
#     A utility class for scraping WeCima, providing methods to extract MP4 URLs,
#     fetch pagination details, and extract series and episode data.
#     """
    
#     def __init__(self):
#         """
#         Initializes the WeCimaScraper with an HTMLSession.
#         """
#         self.session = HTMLSession()
    
#     def extract_mp4s(self, text: str) -> Optional[List[str]]:
#         """
#         Extracts MP4 URLs from the provided text.

#         Args:
#             text (str): The input text containing possible MP4 URLs.

#         Returns:
#             Optional[List[str]]: A list of MP4 URLs if found, otherwise None.
#         """
#         try:
#             pattern = r"https?://.*?\\.mp4"
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
#             base_url (str): The base URL to generate paginated URLs.

#         Returns:
#             List[str]: A list of URLs for each page in the pagination.
#         """
#         try:
#             if not isinstance(total_pages, int) or total_pages < 1:
#                 raise ValueError("total_pages must be a positive integer.")
#             return [f"{base_url}{i}" for i in range(1, total_pages + 1)]
#         except ValueError as e:
#             print(f"Error: {e}")
#             return []

#     def get_series_list_urls(self, pages: List[str], headers: Dict[str, str]) -> List[Dict[str, str]]:
#         """
#         Extracts a list of series from the given paginated URLs, ensuring uniqueness.

#         Args:
#             pages (List[str]): A list of paginated URLs.
#             headers (Dict[str, str]): Headers for the HTTP request.

#         Returns:
#             List[Dict[str, str]]: A list of dictionaries containing series ID, title, and URL.
#         """
#         series_list = []
#         seen_titles = set()
#         count = 0
        
#         try:
#             for page in pages:
#                 response = self.session.get(url=page, headers=headers)
#                 response.raise_for_status()
                
#                 html = response.html.html
#                 parser = HTMLParser(html)
#                 main_grid = parser.css_first("div.Grid--WecimaPosts")
                
#                 if not main_grid:
#                     print(f"Warning: No grid found on {page}")
#                     continue
                
#                 grid_items = main_grid.css("div.GridItem")
                
#                 for item in grid_items:
#                     title = item.css_first("a").attributes.get("title", "Unknown").strip()
#                     url = item.css_first("a").attributes.get("href", "#").strip()
                    
#                     if title not in seen_titles:
#                         seen_titles.add(title)
#                         count += 1
#                         series_list.append({"id": count, "title": title, "url": url})
            
#             return series_list if series_list else []
        
#         except RequestError as e:
#             print(f"HTTP request error: {e}")
#             return []
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             return []
    
#     def get_episodes_list(self, url: str, headers: Dict[str, str]) -> List[str]:
#         """
#         Extracts a list of episode URLs from a given series page.

#         Args:
#             url (str): The URL of the series page.
#             headers (Dict[str, str]): Headers for the HTTP request.

#         Returns:
#             List[str]: A list of episode URLs.
#         """
#         try:
#             response = self.session.get(url=url, headers=headers)
#             response.raise_for_status()
            
#             html = response.html.html
#             parser = HTMLParser(html)
#             main_grid = parser.css_first("div.Episodes--Seasons--Episodes")
            
#             if not main_grid:
#                 print(f"Warning: No episodes found on {url}")
#                 return []
            
#             anchors = main_grid.css("a")
#             episodes = [a.attributes["href"].strip() for a in anchors]
            
#             return episodes[::-1] if episodes else []
        
#         except RequestError as e:
#             print(f"HTTP request error: {e}")
#             return []
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             return []

# # Example usage
# scraper = WeCimaScraper()


import re
from typing import List, Optional, Dict
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser

class WeCimaScraper:
    """
    A utility class for scraping WeCima, providing methods to extract MP4 URLs,
    fetch pagination details, and extract series and episode data.
    """
    
    def __init__(self):
        """
        Initializes the WeCimaScraper with an HTMLSession.
        """
        self.session = HTMLSession()
    
    def extract_mp4s(self, text: str) -> Optional[List[str]]:
        """
        Extracts MP4 URLs from the provided text.

        Args:
            text (str): The input text containing possible MP4 URLs.

        Returns:
            Optional[List[str]]: A list of MP4 URLs if found, otherwise None.
        """
        try:
            pattern = r"https?://.*?\\.mp4"
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
            base_url (str): The base URL to generate paginated URLs.

        Returns:
            List[str]: A list of URLs for each page in the pagination.
        """
        try:
            if not isinstance(total_pages, int) or total_pages < 1:
                raise ValueError("total_pages must be a positive integer.")
            return [f"{base_url}{i}" for i in range(1, total_pages + 1)]
        except ValueError as e:
            print(f"Error: {e}")
            return []

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
        seen_titles = set()
        count = 0
        
        try:
            for page in pages:
                response = self.session.get(url=page, headers=headers)
                response.raise_for_status()
                
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
                    
                    if title not in seen_titles:
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
    
    def get_episodes_list(self, url: str, headers: Dict[str, str]) -> List[str]:
        """
        Extracts a list of episode URLs from a given series page.

        Args:
            url (str): The URL of the series page.
            headers (Dict[str, str]): Headers for the HTTP request.

        Returns:
            List[str]: A list of episode URLs.
        """
        try:
            response = self.session.get(url=url, headers=headers)
            response.raise_for_status()
            
            html = response.html.html
            parser = HTMLParser(html)
            main_grid = parser.css_first("div.Episodes--Seasons--Episodes")
            
            if not main_grid:
                print(f"Warning: No episodes found on {url}")
                return []
            
            anchors = main_grid.css("a")
            episodes = [a.attributes["href"].strip() for a in anchors]
            
            return episodes[::-1] if episodes else []
        
        except RequestError as e:
            print(f"HTTP request error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def get_mp4s(self, url: str, headers: Dict[str, str]) -> List[str]:
        """
        Extracts MP4 download links from a given episode URL.

        Args:
            url (str): The URL of the episode page.
            headers (Dict[str, str]): Headers for the HTTP request.

        Returns:
            List[str]: A list of MP4 download URLs.
        """
        try:
            response = self.session.get(url=url, headers=headers)
            response.raise_for_status()
            
            html = response.html.html
            parser = HTMLParser(html)
            ul = parser.css_first("ul.List--Download--Wecima--Single")
            
            if not ul:
                print(f"Warning: No download list found on {url}")
                return []
            
            lis = ul.css("li")
            anchors = [li.css_first("a.hoverable").attributes["href"].strip() for li in lis]
            
            return anchors if anchors else []
        
        except RequestError as e:
            print(f"HTTP request error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

# Example usage
scraper = WeCimaScraper()
