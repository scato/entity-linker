import os
from entity_linker.data.file import LOCAL_ROOT
import gzip
import mwparserfromhell
import json


def resolve_alias(title, aliases):
    if title in aliases:
        return aliases[title]

    return title


def feature_files_are_present(*data_sets):
    for data_set in data_sets:
        if not os.path.isdir('{}/{}'.format(LOCAL_ROOT, data_set)):
            return False

    return True


def write_features(pages, aliases, data_set):
    os.makedirs('{}/{}'.format(LOCAL_ROOT, data_set), exist_ok=True)

    labels_filename = '{}/{}/labels.json.gz'.format(LOCAL_ROOT, data_set)
    mentions_filename = '{}/{}/mentions.json.gz'.format(LOCAL_ROOT, data_set)
    outgoing_filename = '{}/{}/outgoing.json.gz'.format(LOCAL_ROOT, data_set)
    linked_entities_filename = '{}/{}/linked_entities.json.gz'.format(LOCAL_ROOT, data_set)

    with gzip.open(labels_filename, mode='wt') as labels_fp:
        with gzip.open(mentions_filename, mode='wt') as mentions_fp:
            with gzip.open(linked_entities_filename, mode='wt') as linked_entities_fp:
                with gzip.open(outgoing_filename, mode='wt') as outgoing_fp:
                    for title, text in pages:
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

                        json.dump({'entity_id': title, 'outgoing_entity_ids': linked_entities}, outgoing_fp)
                        outgoing_fp.write('\n')

                        json.dump({'text': plain_text, 'linked_entity_ids': linked_entities}, linked_entities_fp)
                        linked_entities_fp.write('\n')
