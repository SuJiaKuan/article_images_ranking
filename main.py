import argparse
import os

from article_images_ranking.article import load_articles
from article_images_ranking.io import download_file
from article_images_ranking.io import mkdir_p
from article_images_ranking.io import save_json
from article_images_ranking.math import cal_cosine
from article_images_ranking.model import ImageCaptioning
from article_images_ranking.model import SentenceEncoder


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


def rank_article_images(
    article,
    image_captioning,
    sentence_encoder,
    out_dir,
):
    title_vector = sentence_encoder.encode(article.title)

    scores = []
    for image_idx, image_url in enumerate(article.image_urls):
        # TODO (SuJiaKaun):
        # 1. Check is there any another type of images (ex: png) to download?
        # 2. Skip invalid images, such as small logo, empty images.
        image_path = os.path.join(
            out_dir,
            '{}.{}'.format(image_idx, image_url.extension),
        )
        download_file(image_url.url, image_path)

        sentences = image_captioning.generate(image_path)
        # TODO (SuJiaKuan):
        # How to use all generated sentences, instead of just fixed one?
        sentence = sentences[0][1]

        sentence_vector = sentence_encoder.encode(sentence)
        similarity = cal_cosine(title_vector, sentence_vector)

        scores.append((image_path, image_url.url, sentence, similarity))

    scores = sorted(scores, key=lambda r: r[2], reverse=True)

    return {
        'title': article.title,
        'scores': scores,
    }


def main(args):
    articles = load_articles(args.data)

    image_captioning = ImageCaptioning(
        args.caption_rnn,
        args.caption_cnn,
        args.caption_vocab,
    )
    sentence_encoder = SentenceEncoder()

    for article_idx, article in enumerate(articles):
        out_dir = os.path.join(args.output, str(article_idx))

        mkdir_p(out_dir)

        try:
            result = rank_article_images(
                article,
                image_captioning,
                sentence_encoder,
                out_dir,
            )
        except Exception as e:
            print('Fail to rank article {} due to error: {}'
                  .format(article_idx, e))
            continue

        print('==== Ranking for article {} ===='.format(article_idx))
        print('Title: {}'.format(result['title']))
        print('Scores:')
        for score in result['scores']:
            print(score)

        result_path = os.path.join(out_dir, 'result.json')
        save_json(result, result_path)

        print('Result saved in {}'.format(result_path))


if __name__ == '__main__':
    main(parse_args())
