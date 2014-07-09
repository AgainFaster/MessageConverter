#!/usr/bin/env python
from functools import reduce
import csv
import operator
from collections import OrderedDict
import logging
import io

logging.basicConfig(level=logging.DEBUG)


class Dict2Csv(object):
    """Process a JSON object to a CSV file"""
    collection = None

    def __init__(self, outline):
        self.rows = []

        if not type(outline) is dict:
            raise ValueError('You must pass in an outline for JSON2CSV to follow')
        elif 'map' not in outline or len(outline['map']) < 1:
            raise ValueError('You must specify at least one value for "map"')

        key_map = OrderedDict()
        for header, key in outline['map']:
            splits = key.split('.')
            splits = [int(s) if s.isdigit() else s for s in splits]
            key_map[header] = splits

        self.key_map = key_map
        if 'collection' in outline:
            self.collection = outline['collection']

    def process_each_item_as_row(self, data):
        """Process each item of a json-loaded dict
        """
        if self.collection and self.collection in data:
            data = data[self.collection]

        for d in data:
            logging.info(d)
            self.rows.append(self.process_row(d))

    def process_row(self, item):
        """Process a row of json data against the key map
        """
        row = {}

        for header, keys in self.key_map.items():
            try:
                row[header] = reduce(operator.getitem, keys, item)
            except (KeyError, TypeError):
                row[header] = None

        return row

    def write_csv(self, filename='output.csv', write_header_row=True):
        """Write the processed rows to the given filename
        """
        if (len(self.rows) <= 0):
            raise AttributeError('No rows were loaded')
        with open(filename, 'w+', newline='') as f:
            writer = csv.DictWriter(f, self.key_map.keys())
            if write_header_row:
                writer.writeheader()
            writer.writerows(self.rows)


    def write_string(self, write_header_row=True):
        """Write the processed rows to the given filename
        """
        if (len(self.rows) <= 0):
            raise AttributeError('No rows were loaded')

        output = io.StringIO()

        writer = csv.DictWriter(output, self.key_map.keys())
        if write_header_row:
            writer.writeheader()
        writer.writerows(self.rows)

        return output.getvalue()


