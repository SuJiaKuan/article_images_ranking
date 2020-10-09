import argparse
import os

import pandas as pd

from article_images_ranking.io import load_json


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script to evaluate the ranking result',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'ref_path',
        type=str,
        help='Path to the Pixnet articles file',
    )
    parser.add_argument(
        'ranking_path',
        type=str,
        help='Path to the directory of ranking result',
    )
    parser.add_argument(
        '-k',
        type=int,
        default=5,
        help='Value of K for recall metric',
    )

    args = parser.parse_args()

    return args


def load_representatives(ref_path):
    return list(pd.read_csv(ref_path)['top_1'])


def load_rankings(representatives, ranking_path):
    rankings = []

    for article_idx in range(len(representatives)):
        result_path = os.path.join(
            ranking_path,
            str(article_idx),
            'result.json',
        )
        rankings.append(load_json(result_path))

    return rankings


def evaluate_recall(representatives, rankings, k):
    cnt_correct = 0
    cnt_total = 0

    for representative, ranking in zip(representatives, rankings):
        image_top_k = [s[0] for s in ranking['scores'][0:k]]
        image_top_k = [
            int(i.split('/')[-1].split('.')[0])
            for i
            in image_top_k
        ]
        if representative in image_top_k:
            cnt_correct += 1

        cnt_total += 1

    return cnt_correct / cnt_total


def evaluate(representatives, rankings, k):
    scores = {}

    scores['recall @{}'.format(k)] = evaluate_recall(
        representatives,
        rankings,
        k,
    )

    return scores


def main(args):
    representatives = load_representatives(args.ref_path)
    rankings = load_rankings(representatives, args.ranking_path)

    scores = evaluate(representatives, rankings, args.k)

    print(scores)


if __name__ == '__main__':
    main(parse_args())
