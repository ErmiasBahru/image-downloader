#!/usr/bin/python3

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import argparse


def is_valid(url):
    """check whether the url is a valid URL."""

    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    """Returns all image URLs"""

    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all('img'), 'extracting images...'):
        imgUrl = img.attrs.get('src')
        if not imgUrl:
            # if img does not contain src, skip
            continue
        imgUrl = urljoin(url, imgUrl)

        try:
            pos = imgUrl.index('?')
            imgUrl = imgUrl[:pos]
        except ValueError:
            pass

        if is_valid(imgUrl):
            urls.append(imgUrl)
    return urls


def download(url, pathname):
    if not os.path.isdir(pathname):
        os.mkdir(pathname)

    resp = requests.get(url, stream=True)

    # get total file size
    file_size = int(resp.headers.get('Content-Length', 0))

    # get file name
    filename = os.path.join(pathname, url.split("/")[-1])

    progressBar = tqdm(resp.iter_content(
        1024), f"downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as fn:
        for data in progressBar.iterable:
            fn.write(data)
            # update progress bar
            progressBar.update(len(data))


def main(url, path):
    imgs = get_all_images(url)
    for img in imgs:
        download(img, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="a python script that download all images from a web page")
    parser.add_argument(
        "url", help="the URL of the web page you want to dwonload images")
    parser.add_argument(
        "-p", "--path", help="the directory you want to store your images, default is the doain of URL")

    args = parser.parse_args()
    url = args.url
    path = args.path

    if not path:
        # if the path is not speciefied, use the domain name of that url as a folder name
        path = urlparse(url).netloc

    main(url, path)
