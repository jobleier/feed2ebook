import feedparser
import pypandoc
import sys
from datetime import datetime
from time import mktime

if len(sys.argv) is not 2:
    print "usage: feed2ebook.py <url>"
    exit()

ascii = lambda x: x.encode('ascii', 'xmlcharrefreplace')
metadata = lambda title, author, addition: '% ' + title + '\n% ' + author + '\n% ' + addition + '\n\n'

d = feedparser.parse(sys.argv[1])
feed = d.feed.title
for item in d.entries:
    title = ascii(item.title)
    output = "<html><body>\n"
    for content in item.content:
        output += ascii(content.value) + "\n"
    else:
        output += ascii(item.description) + "\n"
    output += "</body></html>\n"

    # bypass over markdown to add title information without writing extra metadata file
    md_output = pypandoc.convert_text(output, 'markdown', format='html')
    display_date = item.published
    md_output = metadata(title, feed, display_date) + md_output

    name_date = datetime.fromtimestamp(mktime(item.published_parsed)).strftime('%Y-%m-%dT%H:%M:%S')
    filename = feed + ' ' + name_date + '.epub'
    pypandoc.convert_text(md_output, 'epub3', format='markdown', outputfile=filename)
