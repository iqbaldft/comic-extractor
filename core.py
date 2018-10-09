#! .venv/bin/python3

import os
from urllib.request import urlretrieve

import requests


class ComicScrapper:
    def __init__(self, url, directory_name, record_file='records.txt'):
        self.url = url
        self.directory = 'downloads/{}'.format(directory_name.strip())
        self.index = 1
        self.record_file = record_file

    def get_page(self):
        """Get page contents from a url
        :return: string page contents
        """
        page = requests.get(self.url)
        return page.content if page.status_code == 200 else None

    def download_image(self, image_url):
        """Download image from url
        """
        filename = image_url.split('/')[-1]
        filename = '{}-{}'.format(self.index, filename)
        full_path = '{}/{}'.format(self.directory, filename)
        urlretrieve(image_url, full_path)
        return filename

    def record(self, rec):
        filename = '{}/{}'.format(self.directory, self.record_file)
        with open(filename, 'a+') as record:
            record.write('{}\r\n'.format(rec))

    def check_record(self):
        result = None
        filename = '{}/{}'.format(self.directory, self.record_file)
        if os.path.exists(filename):
            with open(filename, 'r') as record:
                lines = record.readlines()
                result = {
                    'index': len(lines),
                    'url': lines[-1]
                }
        return result

    def get_next_page(self, html_page):
        msg = ("Implement this method !\n"
               "Make sure it return string url of next page, or None")
        raise NotImplementedError(msg)

    def get_comic_img_url(self, html_page):
        msg = ("Implement this method !\n"
               "Make sure it return string url of comic image")
        raise NotImplementedError(msg)

    def run(
            self,
            cont=True,
            verbose_level=0):
        if not os.path.exists(self.directory):
                os.mkdir(self.directory)
        if cont:
            current_record = self.check_record()
            if current_record is not None:
                self.index = current_record['index']+1
                self.url = self.get_next_page(self.get_page())
        while True:
            if not self.url:
                break
            page = self.get_page()
            if page is None:
                break
            img_url = self.get_comic_img_url(page)
            image_name = self.download_image(img_url)
            self.record(self.url)
            if verbose_level == 0:
                print('.', end='')
            elif verbose_level == 1:
                print(self.url)
            elif verbose_level == 2:
                print('{} {}'.format(self.url, image_name))
            self.url = self.get_next_page(page)
            self.index += 1
        print()
        print('Done, result saved in {}'.format(self.directory))
