#! .venv/bin/python3

import os
from urllib.request import urlretrieve

import requests


class ComicScrapper:
    def __init__(self, url, directory_name, record_file='records.txt', base_url=None, image_name=None):
        self.url = url
        self.base_url = base_url or url
        self.directory = 'downloads/{}'.format(directory_name.strip())
        self.index = 1
        self.record_file = record_file
        self.image_name = None
        self.html_page = None

    def get_page(self):
        """Get page contents from a url
        :return: string page contents
        """
        page = requests.get(self.url)
        return page.text if page.status_code == 200 else None

    def get_image_name(self):
        return None

    def download_image(self, image_url):
        """Download image from url
        """
        filename = self.image_name or image_url.split('/')[-1]
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

    def get_next_page(self):
        msg = ("Implement this method !\n"
               "Make sure it return string url of next page, or None")
        raise NotImplementedError(msg)

    def get_comic_img_url(self):
        msg = ("Implement this method !\n"
               "Make sure it return string url of comic image")
        raise NotImplementedError(msg)

    def run(
            self,
            cont=True,
            verbose=0):
        if not os.path.exists(self.directory):
                os.mkdir(self.directory)
        if cont:
            current_record = self.check_record()
            if current_record is not None:
                if verbose == 2:
                    print('Records file found. Attempt to continue from last extraction...')
                self.index = current_record['index']+1
                self.url = current_record['url']
                self.html_page = self.get_page()
                self.url = self.get_next_page()
        while True:
            if not self.url:
                break
            self.html_page = self.get_page()
            if self.html_page is None:
                break
            if verbose == 2:
                print('Downloading from {}'.format(self.url))
            img_url = self.get_comic_img_url()
            self.image_name = self.get_image_name()
            image_name = self.download_image(img_url)
            self.record(self.url)
            if verbose == 0:
                print('.', end='', flush=True)
            elif verbose == 1:
                print(self.url)
            elif verbose == 2:
                print('Saved as {}'.format(image_name))
            self.url = self.get_next_page()
            self.index += 1
        print()
        print('Done, result saved in {}'.format(self.directory))
