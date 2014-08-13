#!/usr/bin/env python
import json
import logging
from io import StringIO

logging.basicConfig(level=logging.DEBUG)


class Csv2Json(object):
    """Process a CSV string to a JSON string"""

    def __init__(self, outline):
        pass

    def convert_to_json(self, csv):

        # Convert 945 x12 EDI CSV document to Shipment JSON that Wombat can understand
        data = {"shipments": []}

        s = StringIO(csv)

        reader = csv.reader(s)
        header_row = None

        for row in reader:
            if row[0] == 'HDR':
                header_row = row
            elif row[0] == 'DTL':
                selected_shipment = None
                tracking_number = row[6]
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
                          "cost": header_row[100],
                          "status": header_row[17],
                          "stock_location": header_row[3],
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
                    "id": row[18],
                    "name": row[12],
                    "product_id": row[12],
                    "quantity": row[22],
                    "price": "?",
                    "options": {}
                })


        s.close()

        return json.dumps(data)