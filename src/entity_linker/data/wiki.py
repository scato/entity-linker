import os
from entity_linker.data.file import LOCAL_ROOT
import gzip
import mwparserfromhell
import json


def resolve_alias(title, aliases):
    if title in aliases:
        return aliases[title]

    return title


def write_features(pages, redirects, data_set):
    os.makedirs('{}/{}'.format(LOCAL_ROOT, data_set), exist_ok=True)

    aliases = dict(redirects)

    with gzip.open('{}/{}/labels.json.gz'.format(LOCAL_ROOT, data_set), mode='wt') as labels_fp:
        with gzip.open('{}/{}/mentions.json.gz'.format(LOCAL_ROOT, data_set), mode='wt') as mentions_fp:
            with gzip.open('{}/{}/linked_entities.json.gz'.format(LOCAL_ROOT, data_set), mode='wt') as linked_entities_fp:
                for index, row in pages.iterrows():
                    title, text = row['title'], row['text']

                    wikicode = mwparserfromhell.parse(text)

                    wikilinks = wikicode.filter_wikilinks()
                    plain_text = wikicode.strip_code()

                    for wikilink in wikilinks:
                        label = {
                            'entity_id': resolve_alias(str(wikilink.title), aliases),
                            'label': str(wikilink.text or wikilink.title)
                        }
                        json.dump(label, labels_fp)
                        labels_fp.write('\n')

                    mentions = [
                        str(wikilink.text or wikilink.title)
                        for wikilink in wikilinks
                    ]
                    json.dump({'text': plain_text, 'mentions': mentions}, mentions_fp)
                    mentions_fp.write('\n')

                    linked_entities = [
                        resolve_alias(str(wikilink.title), aliases)
                        for wikilink in wikilinks
                    ]
                    json.dump({'entity_id': title, 'linked_entity_ids': linked_entities}, linked_entities_fp)
                    linked_entities_fp.write('\n')
