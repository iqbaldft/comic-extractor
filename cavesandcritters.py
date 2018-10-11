#! .venv/bin/python3

import requests
from bs4 import BeautifulSoup

from core import ComicScrapper


class CavesAndCritters(ComicScrapper):
    def get_page(self):
        cookies = {'wp_aoavsv': '18', 'wp_aoavsv_redirect': '0'}
        page = requests.get(self.url, cookies=cookies)
        return page.text if page.status_code == 200 else None

    def get_comic_img_url(self):
        soup = BeautifulSoup(self.html_page, 'html.parser')
        comic_url = (
                soup.find('div', attrs={'class': 'webcomic-image'})
                .find('img')
                .get('src')
            )
        return comic_url

    def get_next_page(self):
        soup = BeautifulSoup(self.html_page, 'html.parser')
        next_page = (
                soup.find('nav', attrs={'role': 'navigation'})
                .find('a', attrs={'class': 'next-webcomic-link'})
                .get('href')
            )
        if next_page != self.url:
            return next_page
        else:
            return None


if __name__ == '__main__':
    comic = CavesAndCritters(
        url='http://cavesandcritters.com/cnc_webcomic/01_000/',
        directory_name='cavesandcritters'
    )
    comic.run(verbose=1)
