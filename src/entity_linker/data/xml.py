from xml.etree.ElementTree import iterparse
from bz2 import BZ2File
from entity_linker.data.file import LOCAL_ROOT


def read_redirects(filename):
    fp = BZ2File('{}/{}'.format(LOCAL_ROOT, filename))

    for event, elem in iterparse(fp, events=['start', 'end']):
        if event == 'start' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}mediawiki':
            root = elem

        if event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
            redirect = elem.find('{http://www.mediawiki.org/xml/export-0.10/}redirect')
            ns = elem.find('{http://www.mediawiki.org/xml/export-0.10/}ns')

            if redirect is not None and ns.text == '0':
                title = elem.find('{http://www.mediawiki.org/xml/export-0.10/}title')

                yield (title.text, redirect.attrib['title'])

            root.clear()


def read_pages(filename):
    fp = BZ2File('{}/{}'.format(LOCAL_ROOT, filename))

    for event, elem in iterparse(fp, events=['start', 'end']):
        if event == 'start' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}mediawiki':
            root = elem

        if event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
            redirect = elem.find('{http://www.mediawiki.org/xml/export-0.10/}redirect')
            ns = elem.find('{http://www.mediawiki.org/xml/export-0.10/}ns')

            if redirect is None and ns.text == '0':
                title = elem.find('{http://www.mediawiki.org/xml/export-0.10/}title')
                revision = elem.find('{http://www.mediawiki.org/xml/export-0.10/}revision')
                text = revision.find('{http://www.mediawiki.org/xml/export-0.10/}text')

                yield (title.text, text.text)

            root.clear()
