#! .venv/bin/python3

from bs4 import BeautifulSoup

import core


def get_comic_img_url(html_page):
    """Get url of comic image
    :param html_page: string html page of the comic
    :return: URL of the comic image
    """
    soup = BeautifulSoup(html_page, 'html.parser')
    comic_url = soup.find('div', attrs={'id': 'comic'}).find('img').get('src')
    return comic_url


def get_next_page(html_page):
    """Get next comic page
    :param html_page: string html page of the comic
    :return: URL of next comic page
    """
    soup = BeautifulSoup(html_page, 'html.parser')
    next_page = (soup.find('table', attrs={'class': 'comic_navi'})
                     .find('a', attrs={'class': 'navi-next'}))
    result = next_page.get('href') if next_page else None
    return result


if __name__ == '__main__':
    core.run(
        page_url='http://www.housepetscomic.com/comic/2018/10/08/talking-to-the-camera/',
        save_dir='housepets_test',
        get_next_page=get_next_page,
        get_comic_img_url=get_comic_img_url
    )
