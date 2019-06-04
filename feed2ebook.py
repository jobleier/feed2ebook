import feedparser
import pypandoc
import sys
from datetime import datetime
from time import mktime

if len(sys.argv) is not 2:
    print "usage: feed2ebook.py <url>"
    exit()

d = feedparser.parse(sys.argv[1])
feed = d.feed.title
for item in d.entries:
    ascii = lambda x: x.encode('ascii', 'xmlcharrefreplace')
    title = ascii(item.title)
    output = "---\n"
    output = "title: '" + feed + "'\n"
    output = "---\n"
    output += "<h2>" + title + "</h2>\n"
    for content in item.content:
        output += ascii(content.value) + "\n"
    else:
        output += ascii(item.description) + "\n"
    date = datetime.fromtimestamp(mktime(item.published_parsed)).strftime('%Y-%m-%dT%H:%M:%S')
    filename = feed + ' ' + date + '.epub'
    pypandoc.convert_text(output, 'epub3', format='html', outputfile=filename)
