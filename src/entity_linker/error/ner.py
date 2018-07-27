import numpy as np
import sys

from gensim.matutils import sparse2full
from sklearn.metrics import precision_score, recall_score

from entity_linker import mentions
from entity_linker.data.dict import load_mention_dict
from entity_linker.data.json import read_json_data


def doc2clipped(doc, dictionary):
    bow = dictionary.doc2bow(doc)
    vec = sparse2full(bow, len(dictionary))

    return np.clip(vec, 0, 1)


def calculate_metric_for_record(record, metric):
    dictionary = load_mention_dict()

    entities_true = doc2clipped(record['mentions'], dictionary)
    entities_pred = doc2clipped(mentions(record['text']), dictionary)

    return metric(entities_true, entities_pred)


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
    if len(sys.argv) < 2:
        print('usage: python -m {} data_set'.format(__spec__.name))
        exit(1)

    data_set = sys.argv[1]

    print('Calculating NER metrics for "{}" data set...'.format(data_set))

    precision = calculate_metric(data_set, precision_score)
    print('Precision: {}'.format(precision))

    recall = calculate_metric(data_set, recall_score)
    print('Recall: {}'.format(recall))
