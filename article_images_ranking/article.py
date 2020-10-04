import json

import pandas as pd

from article_images_ranking.io import load_jsonl
from article_images_ranking.math import is_nan


_IMAGE_EXTENSION_MAPPING = {
    '.jpg': 'jpg',
    '.jpeg': 'jpg',
    '.png': 'png',
    '.gif': 'gif',
}


class ImageUrl(object):

    def __init__(self, url):
        self._original_url = url

        self._url = self._correct_url(self._original_url)
        self._extension = self._parse_extension(self._url)

    @property
    def url(self):
        return self._url

    @property
    def extension(self):
        return self._extension

    def _correct_url(self, url):
        return 'https:{}'.format(url) if url.startswith('//') else url

    def _parse_extension(self, url):
        for extension_str, extension in _IMAGE_EXTENSION_MAPPING.items():
            if extension_str in url:
                return extension

        raise ValueError('No supported image extension for {}'.foramt(url))


class Article(object):

    def __init__(self, title, image_urls):
        self._title = title
        self._image_urls = [ImageUrl(u) for u in image_urls]

    @property
    def title(self):
        return self._title

    @property
    def image_urls(self):
        return self._image_urls


def load_articles(data_path):
    if data_path.endswith('.json'):
        raw_articles = load_jsonl(data_path)
    elif data_path.endswith('.csv'):
        raw_articles = pd.read_csv(data_path)
        raw_articles = [a for _, a in raw_articles.iterrows()]
    else:
        raise ValueError('Non-Supported data type: {}'.foramt(data_path))

    articles = []

    for raw_article in raw_articles:
        title = raw_article['title']

        if 'image_links' not in raw_article:
            image_links = '[]'
        elif is_nan(raw_article['image_links']):
            image_links = '[]'
        else:
            image_links = raw_article['image_links']
        image_urls = [im['url'] for im in json.loads(image_links)]

        articles.append(Article(title, image_urls))

    return articles
