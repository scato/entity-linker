import logging

import numpy as np
import sys

from gensim.matutils import sparse2full
from sklearn.metrics import precision_score, recall_score

from entity_linker.model.ner import mentions
from entity_linker.data.dict import load_mention_dict
from entity_linker.data.json import read_json_data


def doc2clipped(doc, dictionary):
    bow = dictionary.doc2bow(doc)
    vec = sparse2full(bow, len(dictionary))

    return np.clip(vec, 0, 1)


def calculate_metric_for_record(record, metric):
    dictionary = load_mention_dict()

    mentions_true_doc = record['mentions']
    mentions_pred_doc = mentions(record['text'])

    logger = logging.getLogger('entity_linker')
    logger.debug('Expected mentions: {}'.format(mentions_true_doc))
    logger.debug('Actual mentions: {}'.format(mentions_pred_doc))

    mentions_true = doc2clipped(mentions_true_doc, dictionary)
    mentions_pred = doc2clipped(mentions_pred_doc, dictionary)

    return metric(mentions_true, mentions_pred)


def calculate_metric(data_set, metric):
    data = read_json_data(data_set, 'mentions.json.gz')

    # collect metrics for all of the records
    metrics = np.fromiter(
        (calculate_metric_for_record(record, metric) for record in data),
        dtype=np.float64
    )

    # take the average over all records
    return np.average(metrics)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    if len(sys.argv) < 2:
        print('usage: python -m {} data_set'.format(__spec__.name))
        exit(1)

    data_set = sys.argv[1]

    print('Calculating NER metrics for "{}" data set...'.format(data_set))

    precision = calculate_metric(data_set, precision_score)
    recall = calculate_metric(data_set, recall_score)

    print('Precision: {}'.format(precision))
    print('Recall: {}'.format(recall))
