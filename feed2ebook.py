import errno
import feedparser
import os
import pypandoc
import sys
from datetime import datetime
from time import mktime

xml_ascii = lambda x: x.encode('ascii', 'xmlcharrefreplace')
text_ascii = lambda x: x.encode('ascii', 'replace')
metadata = lambda title, author, addition: '% ' + title + '\n% ' + author + '\n% ' + addition + '\n\n'
filename = lambda x: text_ascii(x).replace('/', '-')

def safely_create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if len(sys.argv) is not 2:
    print "usage: feed2ebook.py <url>"
    exit()

d = feedparser.parse(sys.argv[1])
feed = d.feed.title
safely_create_dir(filename(feed))
for item in d.entries:
    title = xml_ascii(item.title)
    output = "<html><body>\n"
    for content in item.content:
        output += xml_ascii(content.value) + "\n"
    else:
        output += xml_ascii(item.description) + "\n"
    output += "</body></html>\n"

    # bypass over markdown to add title information without writing extra metadata file
    md_output = pypandoc.convert_text(output, 'markdown', format='html')
    display_date = item.published
    md_output = metadata(title, feed, display_date) + md_output

    name_date = datetime.fromtimestamp(mktime(item.published_parsed)).strftime('%Y-%m-%d')
    name = feed + '/' + name_date + ' ' + filename(item.title) + '.epub'
    pypandoc.convert_text(md_output, 'epub3', format='markdown', outputfile=name)
