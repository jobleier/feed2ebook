import errno
import feedparser
import os
import pypandoc
import sys

from datetime import datetime, timedelta
from time import mktime


def xml_ascii(x): return x.encode('ascii', 'xmlcharrefreplace')


def text_ascii(x): return x.encode('ascii', 'replace')


def create_metadata(title, author, addition): return '% ' + \
    title + '\n% ' + author + '\n% ' + addition + '\n\n'


def to_filename(x): return text_ascii(x).replace('/', '-')


def timestamp(dt): return (dt - datetime(1970, 1, 1)).total_seconds()


def safely_create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_ebook(item, feed_title, feed_folder):
    title = xml_ascii(item.title)
    output = "<html>\n<body>\n"
    for content in item.content:
        output += xml_ascii(content.value) + "\n"
    else:
        output += xml_ascii(item.description) + "\n"
    output += "</body>\n</html>\n"

    # bypass over markdown to add title information without writing extra metadata file
    md_output = pypandoc.convert_text(output, 'markdown', format='html')
    md_output = create_metadata(title, feed_title, item.published) + md_output

    published = datetime.fromtimestamp(
        mktime(item.published_parsed)).strftime('%Y-%m-%d')
    name = feed_folder + '/' + published + \
        ' ' + to_filename(item.title) + '.epub'
    pypandoc.convert_text(md_output, 'epub3',
                          format='markdown', outputfile=name)


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print("usage: feed2ebook.py <url>")
        exit()

    current_update = datetime.now()
    d = feedparser.parse(sys.argv[1])
    feed_title = d.feed.title
    feed_folder = to_filename(feed_title)
    safely_create_dir(feed_folder)

    if os.path.isfile(feed_folder + '/.feed2ebook'):
        with open(feed_folder + '/.feed2ebook') as persistent:
            last_update = float(persistent.read())
    else:
        last_update = timestamp(datetime.min)

    for item in d.entries:
        item_time = mktime(item.published_parsed)
        if item_time > last_update:
            create_ebook(item, feed_title, feed_folder)

    with open(feed_folder + '/.feed2ebook', 'w') as persistent:
        persistent.write(str(timestamp(current_update)))
