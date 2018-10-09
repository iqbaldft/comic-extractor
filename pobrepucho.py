#! .venv/bin/python3

from bs4 import BeautifulSoup

from core import ComicScrapper


class PobrePucho(ComicScrapper):
    def get_comic_img_url(self):
        soup = BeautifulSoup(self.html_page, 'html.parser')
        comic_url = (
                soup.find('img', attrs={'id': 'comicimage'})
                .get('src')
            )
        return comic_url

    def get_next_page(self):
        soup = BeautifulSoup(self.html_page, 'html.parser')
        next_page = (
                soup.find('div', attrs={'id': 'comicnav'})
                .find('a', attrs={'rel': 'next'})
            )
        next_url = '{}{}'.format(self.base_url, next_page.get('href'))
        if next_page != self.url:
            return next_url
        else:
            return None

    def get_image_name(self):
        soup = BeautifulSoup(self.html_page, 'html.parser')
        image_extension = (
                soup.find('img', attrs={'id': 'comicimage'})
                .get('src')
                .split('.')[-1]
            )
        image_name = (
            soup.find('h2', attrs={'class': 'heading'})
            .string
        )
        return '{}.{}'.format(image_name, image_extension)


if __name__ == '__main__':
    comic = PobrePucho(
        url='http://www.pobrepucho.thecomicseries.com/comics/1',
        directory_name='pobrepucho',
        base_url='http://www.pobrepucho.thecomicseries.com'
    )
    comic.run(verbose_level=1)
