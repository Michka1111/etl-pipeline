import requests
from bs4 import BeautifulSoup

class RawHTMLExtractor:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_html(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def extract_text(self, html, tag='body'):
        soup = BeautifulSoup(html, 'html.parser')
        main = soup.find(tag)
        return main.get_text(separator='\n', strip=True) if main else html

    def get_raw_text(self, url, tag='body'):
        html = self.fetch_html(url)
        return self.extract_text(html, tag)
