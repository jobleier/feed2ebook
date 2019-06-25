# feed2ebook

Creates an epub file for each entry of a given RSS or Atom feed.
The idea is to read news feeds or blogs in a comfortable way on an ebook reader without the need of wifi.
Having one file for each entry makes it easy to track already read articles.

## Usage

The script takes one argument with the path or url to a RSS or Atom feed.

```
usage: feed2ebook.py [-h] url

convert feed to separat ebooks

positional arguments:
  url         file or url of RSS or Atom feed

optional arguments:
  -h, --help  show this help message and exit
```

## What it does

The script reads a RSS or Atom feed from a given url, parses the content and creates one epub file for each entry in a directory named by the feeds title.
To avoid duplicate entries, it stores the time of the last update and ignores entries created before.

## How it works

It reads the feed using feedparser and converts the html encoded content to epub using pandoc.

## Setup

Install prerequisites for Ubuntu (tested with 18.04):

```
sudo apt install pandoc python-pypandoc python-feedparser
```
