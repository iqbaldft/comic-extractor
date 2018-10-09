#! .venv/bin/python

import os
import shutil
import unittest

from bs4 import BeautifulSoup

from housepets import Housepets


class TestHousepets(unittest.TestCase):
    def setUp(self):
        self.url = 'http://www.housepetscomic.com/comic/2008/06/02/when-boredom-strikes/'
        self.directory_name = 'test_housepets'
        if not os.path.exists('downloads/{}'.format(self.directory_name)):
                os.mkdir('downloads/{}'.format(self.directory_name))
        self.comic = Housepets(
            url=self.url,
            directory_name=self.directory_name
        )

    def tearDown(self):
        if os.path.exists('downloads/{}'.format(self.directory_name)):
            shutil.rmtree('downloads/{}'.format(self.directory_name))

    def test_get_page(self):
        page = self.comic.get_page()
        self.assertIsInstance(page, str)
        self.assertIn('<html', page)
        self.assertIn('</html>', page)
        soup = BeautifulSoup(page, 'html.parser')
        self.assertIsNotNone(soup)

    def test_get_comic_img_url(self):
        page = self.comic.get_page()
        comic_img_url = self.comic.get_comic_img_url(page)
        self.assertIn('http', comic_img_url)

    def test_download_image(self):
        page = self.comic.get_page()
        comic_img_url = self.comic.get_comic_img_url(page)
        filename = self.comic.download_image(comic_img_url)
        self.assertIsInstance(filename, str)
        self.assertTrue(os.path.exists('downloads/{}/{}'.format(self.directory_name, filename)))

    def test_record(self):
        self.comic.record('test')
        self.assertTrue(os.path.exists('downloads/{}/records.txt'.format(self.directory_name)))
        check_record = self.comic.check_record()
        self.assertDictEqual(check_record, {'index': 1, 'url': 'test\n'})

    def test_get_next_page(self):
        page = self.comic.get_page()
        next_page = self.comic.get_next_page(page)
        self.assertIn('http', next_page)


if __name__ == '__main__':
    unittest.main()
