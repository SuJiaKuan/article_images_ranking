import argparse
import json
import os

from article_images_ranking.io import download_file
from article_images_ranking.io import load_jsonl
from article_images_ranking.model import ImageCaptioning


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
        '--caption_rnn',
        type=str,
        default='./data/caption_en_model40.model',
        help='Path to the RNN model for image captioning',
    )
    parser.add_argument(
        '--caption_cnn',
        type=str,
        default='./data/ResNet50.model',
        help='Path to the CNN model for image captioning',
    )
    parser.add_argument(
        '--caption_vocab',
        type=str,
        default='./third_party/chainer-caption/data/MSCOCO/'
                'mscoco_caption_train2014_processed_dic.json',
        help='Path to the vocabulary for image captioning',
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


def rank_article_images(article, article_id, image_captioning, out_dir):
    image_urls = [im['url'] for im in json.loads(article['image_links'])]
    for image_idx, image_url in enumerate(image_urls):
        # TODO (SuJiaKaun):
        # 1. Check is there any another type of images (ex: png) to download?
        # 2. Skip invalid images, such as small logo, empty images.
        image_path = os.path.join(
            out_dir,
            article_id,
            '{}.jpg'.format(image_idx),
        )
        download_file(image_url, image_path)

        sentences = image_captioning.generate(image_path)
        print(sentences)


def main(args):
    articles = load_jsonl(args.data)
    articles = load_jsonl(args.data)[0:1]

    image_captioning = ImageCaptioning(
        args.caption_rnn,
        args.caption_cnn,
        args.caption_vocab,
    )

    for article_idx, article in enumerate(articles):
        rank_article_images(
            article,
            str(article_idx),
            image_captioning,
            args.output,
        )


if __name__ == '__main__':
    main(parse_args())
