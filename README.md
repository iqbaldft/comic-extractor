# Comic Extractor
Extract and download images from comic sites  
How to know if a comic site is supported ?  
if the sites had comic image and next button to view next page of the comic,
it has high chance to be supported (well, you still need to implement the extractor by yourself, but still... )

## Requirements
- Python  
I developed this using Python 3.6, untested on other version
- BeautifulSoup4  
Web scraping library for python
- Requests  
Http request library for python
- urllib
for downloading the image

## Installation
(Optional) Using python virtualenv  
```
virtualenv -p python .venv
source .venv/bin/activate
```

install all the requirements package
```
pip install -r requirements.txt
```

## Usage
if using virtualenv, make sure you already activate the virtualenv
```
source .venv/bin/activate
```

for extracting from housepets comic, 
```
python housepets.py
```

## Need support for another comic ?
Why not develop your own function ?  
You need to extend `ComicScrapper` class from `core.py` and implement the `get_next_page` and `get_comic_img_url` function.  
Both function took one argument, which is basically html page in text (string) form.  
`get_next_page` function need to return string of next page url (example : "http://next.page/url/next") or `None` if there is no next page  
`get_comic_img_url` function have to return string comic image url of the param page (example : "http://this.page/url/image.png").  
After all that, instantiate your class (need at least `url` param for first page of the comics, and `directory_name` param for downloaded directory name), and call run() method to start extracting.  
Downloaded files will be in `download` folder in this directory.

## Changelog
- extract from [Housepets!](http://www.housepetscomic.com) comic