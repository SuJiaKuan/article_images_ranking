import argparse
import json
import os

from article_images_ranking.io import download_file
from article_images_ranking.io import load_jsonl


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script to preprocess the news data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'data',
        type=str,
        help='Path to the Pixnet articles JSON Lines file',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='output',
        help='Output folder that contains the generated data',
    )

    args = parser.parse_args()

    return args


def rank_article_images(article, article_id, out_dir):
    image_urls = [im['url'] for im in json.loads(article['image_links'])]
    for image_idx, image_url in enumerate(image_urls):
        # TODO (SuJiaKaun):
        # 1. Check is there any another type of images (ex: png) to download?
        # 2. Skip invalid images, such as small logo, empty images.
        save_path = os.path.join(
            out_dir,
            article_id,
            '{}.jpg'.format(image_idx),
        )
        download_file(image_url, save_path)


def main(args):
    articles = load_jsonl(args.data)

    for article_idx, article in enumerate(articles):
        rank_article_images(article, str(article_idx), args.output)


if __name__ == '__main__':
    main(parse_args())
