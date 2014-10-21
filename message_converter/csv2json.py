#!/usr/bin/env python
import json
import logging
from io import StringIO
import csv

logging.basicConfig(level=logging.DEBUG)


class Csv2Json(object):
    """Process a CSV string to a JSON string"""

    def __init__(self, outline):
        self.outline = outline
        self._row_dict = {}

    def _update_row_dict(self, row, prefix):

        if not prefix:
            self._row_dict = {}
        else:
            # clear anything that starts with the prefix, in case there's not the same number of rows
            for key in self._row_dict:
                if key.startswith('%s.' % prefix):
                    self._row_dict[key] = None

        for i in range(len(row)):
            key = str(i)
            if prefix is not None:
                key = '%s.%s' % (prefix, key)

            self._row_dict[key] = row[i]


    def _get_collection(self, buffer, reader, outline, stop_at_type=None):
        collection_attribute = outline.get('collection')
        collection = {collection_attribute: []}
        data = collection[collection_attribute]

        last_position = buffer.tell()

        for row in reader:
            if not row:
                continue

            if stop_at_type and row[0] == stop_at_type:
                buffer.seek(last_position)
                break

            row_outline = outline.get('outline')

            outline_per_type = outline.get('outline_per_type')
            if not outline_per_type or (outline_per_type and row[0] == outline_per_type):
                row_data = {}

                self._update_row_dict(row, outline_per_type)

                for key in row_outline:
                    if not (key == 'outline' and isinstance(row_outline[key], dict)):
                        row_data[key] = self._row_dict.get(str(row_outline[key]))
                    else:
                        row_data.update(self._get_collection(buffer, reader, row_outline[key], outline_per_type))

                data.append(row_data)

            last_position = buffer.tell()

        return collection

    def convert(self, csv_str):

        s = StringIO(csv_str)
        reader = csv.reader(s, delimiter=',')

        collection = self._get_collection(s, reader, self.outline)

        s.close()
        return json.dumps(collection)

    def convert_edi_945_to_wof_shipment(self, csv_str):

        # Convert 945 x12 EDI CSV document to Shipment JSON that Wombat can understand
        data = {"shipments": []}

        s = StringIO(csv_str)

        reader = csv.reader(s, delimiter='|')
        header_row = None

        for row in reader:
            if row[0] == 'HDR':
                header_row = row
            elif row[0] == 'CNT':
                selected_shipment = None
                tracking_number = row[8] or header_row[42] or header_row[41]  # TrackingNumber, or ProNumber, or BOL

                if not tracking_number:
                    tracking_number = (header_row[30] or '') + '-' + header_row[7]  # CarrierCode-OrderNumber (e.g. FXNL-12345)

                for shipment in data['shipments']:
                    if shipment['tracking'] == tracking_number:
                        selected_shipment = shipment

                if not selected_shipment:
                    name = header_row[21]
                    name_splits = name.split()
                    first_name = name_splits[0]
                    last_name = ' '.join(name_splits[1:])

                    selected_shipment = {
                        "id": tracking_number,
                        "order_id": header_row[7],
                        "email": header_row[22],
                        "carrier": header_row[30],
                        "service": header_row[11],
                        "shipping_method": header_row[31],
                        "tracking": tracking_number,
                        "shipped_at": header_row[9],
                        "shipping_address": {
                            "firstname": first_name,
                            "lastname": last_name,
                            "address1": header_row[23],
                            "address2": header_row[24],
                            "zipcode": header_row[27],
                            "city": header_row[25],
                            "state": header_row[26],
                            "country": header_row[28],
                            "phone": header_row[29]
                          },
                          "items": []
                        }

                    data['shipments'].append(selected_shipment)

                selected_shipment['items'].append({
                    "id": row[12],
                    "product_id": row[13],
                    "quantity": row[19],
                })


        s.close()

        return json.dumps(data)