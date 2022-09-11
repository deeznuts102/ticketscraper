from typing import List
import requests  # type: ignore
import re

BASE_URL = "https://www.ticketswap.com"

class HTMLScraper:

    def _scrape_main_page(self) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "*/*",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.ticketswap.com/",
            "content-type": "application/json",
            "Origin": "https://www.ticketswap.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
        }

        return requests.get(url=BASE_URL, headers=headers)


    def get_session_id(self) -> str:
        response: str = self._scrape_main_page()
        match = re.search("static\/([^\s]+)\/_buildManifest.js", response.text)
        if match and match[1]:
            return match[1]
        else:
            return ""

    def get_event_entrance_type_ids(self, event_uri_path: str, event_uri_id: str, entrance_type: str) -> str:
        ids = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "*/*",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.ticketswap.com/",
            "content-type": "application/json",
            "Origin": "https://www.ticketswap.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
        }

        url = BASE_URL + event_uri_path
        res = requests.get(url, headers=headers)

        match = re.search(f"\/{entrance_type}\/{event_uri_id}\/\d+", res.text).group() # find the entrance type URI id in the href
        return match.split('/')[-1]

