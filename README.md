# Artcile Images Ranking

Ranking for representative images in a Pixnet article.

## Prerequisites

Install following packages for Python 3:

- beautifulsoup4==4.9.1
- chainer==1.24.0
- lxml==4.5.2
- numpy==1.18.1
- pandas==1.1.1
- requests==2.23.0
- tensorflow==2.2.0
- tensorflow_hub==0.8.0
- tensorflow_text==2.2.1

## Steps to Reproduce

* Clone the project

```bash
git clone https://gitlab.com/bataw/article_images_ranking
```

* Change to the project directory

```bash
cd article_images_ranking
```

* Pull submodules for the project

```bash
git submodule update --init
```

* Create the folder for static data

```bash
mkdir -p data
```

* Download the models for image captioning

```bash
 bash third_party/chainer-caption/download.sh
```

* Include Python paths for third party libraries

```bash
export PYTHONPATH=${PYTHONPATH}:third_party/chainer-caption/code
```

* Run the main script with example articles data, and then you will see the results!

```bash
python3 main.py examples/articles.json
```

## TODO

- [ ] Test for for articles (e.g., 滷肉飯)
- [ ] Check and handle different image types of image files (e.g., png)
- [ ] Skip invalid images, such as small logo, empty images
- [ ] Different beam sizes for image captioning and similary comparision
- [ ] Enable GPU
