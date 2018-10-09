#! .venv/bin/python3

import os
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup


def get_page(url):
    """Get page contents from a url
    :param url: URL to get the contents
    :return: string page contents
    """
    page = requests.get(url)
    return page.content if page.status_code == 200 else None


def download_image(url, filename=None, directory='.', index=None):
    """Download image from url, save it as :param filename: in :param directory:
    """
    filename = filename if filename is not None else url.split('/')[-1]
    directory = directory.strip()
    if not os.path.exists(directory):
        os.mkdir(directory)
    if index:
        filename = '{}-{}'.format(index, filename)
    if directory.endswith('/'):
        filename = '{}{}'.format(directory, filename)
    else:
        filename = '{}/{}'.format(directory, filename)
    urlretrieve(url, filename)
    return filename


def record(rec, filename='records.txt', directory='.'):
    if not os.path.exists(directory):
        os.mkdir(directory)
    if directory.endswith('/'):
        filename = '{}{}'.format(directory, filename)
    else:
        filename = '{}/{}'.format(directory, filename)
    with open(filename, 'a+') as record:
        record.write('{}\r\n'.format(rec))


def check_record(filename='records.txt', directory='.'):
    result = None
    if os.path.exists('{}/{}'.format(directory, filename)):
        with open('{}/{}'.format(directory, filename), 'r') as record:
            lines = record.readlines()
            result = {
                'index': len(lines),
                'url': lines[-1]
            }
    return result


def run(
        page_url='',
        save_dir='.',
        cont=True,
        get_next_page=None,
        get_comic_img_url=None,
        verbose_level=0):
    if get_next_page is None:
        print('get_next_page function is not implemented')
        return
    if get_comic_img_url is None:
        print('get_comic_img_url function is not implemented')
        return
    i = 1
    save_dir = 'downloads/{}'.format(save_dir)
    if cont:
        current_record = check_record(directory=save_dir)
        if current_record is not None:
            i = current_record['index']+1
            page_url = get_next_page(get_page(current_record['url']))
    while True:
        if not page_url:
            break
        page = get_page(page_url)
        if page is None:
            break
        img_url = get_comic_img_url(page)
        file_image = download_image(img_url, directory=save_dir, index=i)
        record(page_url, directory=save_dir)
        if verbose_level == 0:
            print('.', end='')
        elif verbose_level == 1:
            print(page_url)
        elif verbose_level == 2:
            print('{} {}'.format(page_url, file_image))
        page_url = get_next_page(page)
        i += 1
    print()
    print('Done, result saved in {}'.format(save_dir))
