import json

from article_images_ranking.io import load_jsonl


class Article(object):

    def __init__(self, title, image_urls):
        self._title = title
        self._image_urls = image_urls

    @property
    def title(self):
        return self._title

    @property
    def image_urls(self):
        return self._image_urls


def load_articles(data_path):
    if data_path.endswith('.json'):
        raw_articles = load_jsonl(data_path)
    else:
        raise ValueError('Non-Supported data type: {}'.foramt(data_path))

    articles = []

    for raw_article in raw_articles:
        title = raw_article['title']
        image_urls = [
            im['url']
            for im
            in json.loads(raw_article.get('image_links', '[]'))
        ]
        articles.append(Article(title, image_urls))

    return articles
