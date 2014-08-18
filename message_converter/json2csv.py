#!/usr/bin/env python
from functools import reduce
import csv
import json
import operator
from collections import OrderedDict
import logging
import io

logging.basicConfig(level=logging.DEBUG)


class Json2Csv(object):
    """Process a JSON object to a CSV file"""
    collection = None
    first_record_header = None

    def __init__(self, outline):
        self.rows = []

        if not type(outline) is dict:
            raise ValueError('You must pass in an outline for JSON2CSV to follow')
        elif 'map' not in outline or len(outline['map']) < 1:
            raise ValueError('You must specify at least one value for "map"')

        key_map = OrderedDict()

        if 'first_record' in outline:
            # every row will be prefixed with the same first_record value
            # store this header as the first header in the key_map
            self.first_record_header, value = outline['first_record']
            key_map[self.first_record_header] = value

        for header, key in outline['map']:
            key_map[header] = self.split_dot_list(key)

        self.key_map = key_map

        if 'collection' in outline:
            self.collection = self.split_dot_list(outline['collection'])

    def split_dot_list(self, str_list):
        splits = str_list.split('.')
        return [int(s) if s.isdigit() else s for s in splits]

    def process_json(self, json_data):
        data = json.loads(json_data)
        self.process(data)

    def process(self, data):
        if self.collection:
            self.process_each_item_as_row(data)
        else:
            self.process_single_item_as_row(data)

    def process_single_item_as_row(self, data):
        """Process a single json-loaded dict
        """
        logging.info(data)
        self.rows.append(self.process_row(data))

    def process_each_item_as_row(self, data):
        """Process each dict of a json-loaded collection
        """
        if self.collection:
            try:
                data = reduce(operator.getitem, self.collection, data)
            except KeyError:
                # move forward anyway
                pass

        for d in data:
            self.process_single_item_as_row(d)

    def process_row(self, item):
        """Process a row of json data against the key map
        """
        row = {}

        for header, keys in self.key_map.items():
            if header == self.first_record_header:
                row[header] = keys
            else:
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

        writer = csv.DictWriter(output, self.key_map.keys(), delimiter='|')
        if write_header_row:
            writer.writeheader()
        writer.writerows(self.rows)

        return output.getvalue()


