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

    def convert(self, csv_str):
        collection_attribute = self.outline['collection']

        collection = {collection_attribute: []}
        data = collection[collection_attribute]

        s = StringIO(csv_str)
        reader = csv.reader(s, delimiter=',')

        attribute_names = self.outline['outline']

        for row in reader:
            row_data = {}
            for i in range(len(row)):
                if i < len(attribute_names):
                    row_data.update({attribute_names[i]: row[i]})
            data.append(row_data)

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