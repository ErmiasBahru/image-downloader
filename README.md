# Download all images from a web page using python

[watch demo](https://vimeo.com/723951707)

### Required:

1. requests
2. bs4
3. tqdm

### Install required dependencies:

```
pip install -r requirements.txt
```

### Usage:

```
python downloader.py --help
```

```
usage: downloader.py [-h] [-p PATH] url

a python script that download all images from a web page

positional arguments:
  url                   the URL of the web page you want to dwonload images

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  the directory you want to store your images, default
                        is the domain of URL

```

### Example:

```
python downloader.py -p ermias https://ermiasbahru.vercel.app/
```
