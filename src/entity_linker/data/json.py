import gzip
import json
import os

from entity_linker.data.file import LOCAL_ROOT


def read_json_data(*paths):
    data_filename = os.path.join(LOCAL_ROOT, *paths)

    with gzip.open(data_filename, mode='rt') as fp:
        for line in fp:
            yield json.loads(line)
