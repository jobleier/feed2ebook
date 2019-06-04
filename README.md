# feed2ebook

Creates an epub file for each entry of a given feed.
The idea is to read news feeds or blogs in a comfortable way on an ebook reader without the need of wifi.
Having one file for each entry makes it easy to track already read articles.

The script takes one argument with the path or url to a rss or atom feed.

## Setup

Install prerequisites for Ubuntu (tested with 18.04):

```
sudo apt install pandoc python-pypandoc python-feedparser
```
