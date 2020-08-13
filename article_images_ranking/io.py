import json
import os
import pathlib
import urllib.request


def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))

    return data


def save_json(obj, file_path, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as f:
        json.dump(obj, f, ensure_ascii=False)


def mkdir_p(dir_path):
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)


def download_file(url, save_path, overwrite=False):
    if os.path.isfile(save_path) and not overwrite:
        return

    mkdir_p(os.path.dirname(save_path))

    urllib.request.urlretrieve(url, save_path)
