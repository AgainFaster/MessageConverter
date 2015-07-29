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
                        "record_type": header_row[0],
                        "customer_id": header_row[1],
                        "company": header_row[2],
                        "warehouse": header_row[3],
                        "load_number": header_row[4],
                        "order_reference_id": header_row[5],
                        "shipping_id": header_row[6],
                        "order_id": header_row[7],
                        "tracking_number": header_row[8],
                        "shipped_at": header_row[9],
                        "commit_date": header_row[10],
                        "service": header_row[11],
                        "lbs": header_row[12],
                        "kgs": header_row[13],
                        "gms": header_row[14],
                        "ozs": header_row[15],
                        "ship_ticket": header_row[16],
                        "height": header_row[17],
                        "width": header_row[18],
                        "length": header_row[19],
                        "ship_to_id_code": header_row[20],
                        "email": header_row[22],
                        "shipping_address": {
                            "firstname": first_name,
                            "lastname": last_name,
                            "contact": header_row[22],
                            "address1": header_row[23],
                            "address2": header_row[24],
                            "city": header_row[25],
                            "state": header_row[26],
                            "zipcode": header_row[27],
                            "country": header_row[28],
                            "phone": header_row[29]
                        },
                        "carrier": header_row[30],
                        "shipping_method": header_row[31],
                        "packet_list_ship_date": header_row[32],
                        "routing": header_row[33],
                        "ship_type": header_row[34],
                        "ship_terms": header_row[35],
                        "reporting_code": header_row[36],
                        "depositor_order": header_row[37],
                        "purchase_order": header_row[38],
                        "delivery_date": header_row[39],
                        "est_delivery": header_row[40],
                        "bill_of_lading": header_row[41],
                        "pro_number": header_row[42],
                        "master_bill_of_lading": header_row[43],
                        "split_ship_number": header_row[44],
                        "invoice_date": header_row[45],
                        "effective_date": header_row[46],
                        "total_units": header_row[47],
                        "total_weight": header_row[48],
                        "uom_weight": header_row[49],
                        "total_volume": header_row[50],
                        "uom_volume": header_row[51],
                        "lading_quantity": header_row[52],
                        "unit_of_measure": header_row[53],
                        "warehouse_name": header_row[54],
                        "warehouse_id": header_row[55],
                        "depositor_name": header_row[56],
                        "depositor_id": header_row[57],
                        "passthru_character_field_1": header_row[58],
                        "passthru_character_field_2": header_row[59],
                        "passthru_character_field_3": header_row[60],
                        "passthru_character_field_4": header_row[61],
                        "passthru_character_field_5": header_row[62],
                        "passthru_character_field_6": header_row[63],
                        "passthru_character_field_7": header_row[64],
                        "passthru_character_field_8": header_row[65],
                        "passthru_character_field_9": header_row[66],
                        "passthru_character_field_10": header_row[67],
                        "passthru_character_field_11": header_row[68],
                        "passthru_character_field_12": header_row[69],
                        "passthru_character_field_13": header_row[70],
                        "passthru_character_field_14": header_row[71],
                        "passthru_character_field_15": header_row[72],
                        "passthru_character_field_16": header_row[73],
                        "passthru_character_field_17": header_row[74],
                        "passthru_character_field_18": header_row[75],
                        "passthru_character_field_19": header_row[76],
                        "passthru_character_field_20": header_row[77],
                        "passthru_num_field_1": header_row[78],
                        "passthru_num_field_2": header_row[79],
                        "passthru_num_field_3": header_row[80],
                        "passthru_num_field_4": header_row[81],
                        "passthru_num_field_5": header_row[82],
                        "passthru_num_field_6": header_row[83],
                        "passthru_num_field_7": header_row[84],
                        "passthru_num_field_8": header_row[85],
                        "passthru_num_field_9": header_row[86],
                        "passthru_num_field_10": header_row[87],
                        "passthru_date_field_1": header_row[88],
                        "passthru_date_field_2": header_row[89],
                        "passthru_date_field_3": header_row[90],
                        "passthru_date_field_4": header_row[91],
                        "passthru_dollar_field_1": header_row[92],
                        "passthru_dollar_field_2": header_row[93],
                        "trailer": header_row[94],
                        "seal": header_row[95],
                        "pallet_count": header_row[96],
                        "freight_cost": header_row[97],
                        "late_ship_reason": header_row[98],
                        "carrier_del_serv": header_row[99],
                        "shipping_cost": header_row[100],
                        "pro_number_or_all_tracking_numbers": header_row[101],
                        "tracking": tracking_number,
                        "items": []
                        }

                    data['shipments'].append(selected_shipment)

                selected_shipment['items'].append({
                    "record_type": row[0],
                    "order_id": row[1],
                    "shipping_id": row[2],
                    "customer_id": row[3],
                    "lpid": row[4],
                    "fromlpid": row[5],
                    "plt_sscc18": row[6],
                    "ctn_sscc18": row[7],
                    "tracking_number": row[8],
                    "link_plt_sscc18": row[9],
                    "link_ctn_sscc18": row[10],
                    "link_tracking_number": row[11],
                    "id": row[12],
                    "product_id": row[13],
                    "lotnumber": row[14],
                    "link_lotnumber": row[15],
                    "useritem1": row[16],
                    "useritem2": row[17],
                    "useritem3": row[18],
                    "quantity": row[19],
                    "unit_of_measure": row[20],
                    "cartons": row[21],
                    "detail_passthru_character_field_1": row[22],
                    "detail_passthru_character_field_2": row[23],
                    "detail_passthru_character_field_3": row[24],
                    "detail_passthru_character_field_4": row[25],
                    "detail_passthru_character_field_5": row[26],
                    "detail_passthru_character_field_6": row[27],
                    "detail_passthru_character_field_7": row[28],
                    "detail_passthru_character_field_8": row[29],
                    "detail_passthru_character_field_9": row[30],
                    "detail_passthru_character_field_10": row[31],
                    "detail_passthru_character_field_11": row[32],
                    "detail_passthru_character_field_12": row[33],
                    "detail_passthru_character_field_13": row[34],
                    "detail_passthru_character_field_14": row[35],
                    "detail_passthru_character_field_15": row[36],
                    "detail_passthru_character_field_16": row[37],
                    "detail_passthru_character_field_17": row[38],
                    "detail_passthru_character_field_18": row[39],
                    "detail_passthru_character_field_19": row[40],
                    "detail_passthru_character_field_20": row[41],
                    "detail_passthru_number_field_1": row[42],
                    "detail_passthru_number_field_2": row[43],
                    "detail_passthru_number_field_3": row[44],
                    "detail_passthru_number_field_4": row[45],
                    "detail_passthru_number_field_5": row[46],
                    "detail_passthru_number_field_6": row[47],
                    "detail_passthru_number_field_7": row[48],
                    "detail_passthru_number_field_8": row[49],
                    "detail_passthru_number_field_9": row[50],
                    "detail_passthru_number_field_10": row[51],
                    "detail_passthru_date_field_1": row[52],
                    "detail_passthru_date_field_2": row[53],
                    "detail_passthru_date_field_3": row[54],
                    "detail_passthru_date_field_4": row[55],
                    "detail_passthru_dollar_field_1": row[56],
                    "detail_passthru_dollar_field_2": row[57],
                    "purchase_order": row[58],
                    "weight": row[59],
                    "volume": row[60],
                })
        s.close()

        return json.dumps(data)

    def convert_edi_944_to_wof_shipment(self, csv_str):

        # Convert 944 x12 EDI CSV document to Shipment JSON that Wombat can understand
        data = {"receipts": []}

        s = StringIO(csv_str)

        reader = csv.reader(s, delimiter=',')
        header_row = None

        for row in reader:
            if row[0] == 'HDR':
                header_row = row
                selected_receipt = None
            elif row[0] == 'DTL':
                if not selected_receipt:
                    shipper_first_name = ""
                    shipper_last_name = ""
                    bill_to_first_name = ""
                    bill_to_last_name = ""

                    shipper_name = header_row[63]
                    shipper_name_splits = shipper_name.split()
                    if shipper_name_splits:
                        shipper_first_name = shipper_name_splits[0]
                        shipper_last_name = ' '.join(name_splits[1:])

                    bill_to_name = header_row[63]
                    bill_to_name_splits = bill_to_name.split()
                    if bill_to_name_splits:
                        bill_to_first_name = bill_to_name_splits[0]
                        bill_to_last_name = ' '.join(name_splits[1:])

                    selected_receipt = {
                        "id": header_row[13],
                        "record_type": header_row[0],
                        "customer": header_row[1],
                        "transaction_set": header_row[2],
                        "direction": header_row[3],
                        "synapse_order_id": header_row[4],
                        "synapse_ship_id": header_row[5],
                        "warehouse_receipt_number": header_row[6],
                        "customer_order_number": header_row[7],
                        "receipt_data": header_row[8],
                        "vendor": header_row[9],
                        "shipping_name": header_row[10],
                        "bol_number": header_row[11],
                        "carrier": header_row[12],
                        "purchase_order_number": header_row[13],
                        "order_type": header_row[14],
                        "total_quantity_expected": header_row[15],
                        "total_quantity_received": header_row[16],
                        "total_quantity_received_in_good_condition":  header_row[17],
                        "total_quantity_received_in_damaged_condition": header_row[18],
                        "date_unloaded": header_row[19],
                        "ship_type": header_row[20],
                        "warehouse_name": header_row[21],
                        "passthru_character_field_1": header_row[22],
                        "passthru_character_field_2": header_row[23],
                        "passthru_character_field_3": header_row[24],
                        "passthru_character_field_4": header_row[25],
                        "passthru_character_field_5": header_row[26],
                        "passthru_character_field_6": header_row[27],
                        "passthru_character_field_7": header_row[28],
                        "passthru_character_field_8": header_row[29],
                        "passthru_character_field_9": header_row[30],
                        "passthru_character_field_10": header_row[31],
                        "passthru_character_field_11": header_row[32],
                        "passthru_character_field_12": header_row[33],
                        "passthru_character_field_13": header_row[34],
                        "passthru_character_field_14": header_row[35],
                        "passthru_character_field_15": header_row[36],
                        "passthru_character_field_16": header_row[37],
                        "passthru_character_field_17": header_row[38],
                        "passthru_character_field_18": header_row[39],
                        "passthru_character_field_19": header_row[40],
                        "passthru_character_field_20": header_row[41],
                        "passthru_num_field_1": header_row[42],
                        "passthru_num_field_2": header_row[43],
                        "passthru_num_field_3": header_row[44],
                        "passthru_num_field_4": header_row[45],
                        "passthru_num_field_5": header_row[46],
                        "passthru_num_field_6": header_row[47],
                        "passthru_num_field_7": header_row[48],
                        "passthru_num_field_8": header_row[49],
                        "passthru_num_field_9": header_row[50],
                        "passthru_num_field_10": header_row[51],
                        "passthru_date_field_1": header_row[52],
                        "passthru_date_field_2": header_row[53],
                        "passthru_date_field_3": header_row[54],
                        "passthru_date_field_4": header_row[55],
                        "passthru_dollar_field_1": header_row[56],
                        "passthru_dollar_field_2": header_row[57],
                        "pro_number": header_row[58],
                        "trailer": header_row[59],
                        "seal": header_row[60],
                        "pallet_count": header_row[61],
                        "facility": header_row[62],
                        "shipper": {
                            "firstname": shipper_first_name,
                            "lastname": shipper_last_name,
                            "contact": header_row[64],
                            "address1": header_row[65],
                            "address2": header_row[66],
                            "zipcode": header_row[67],
                            "city": header_row[68],
                            "state": header_row[69],
                            "country": header_row[70],
                            "phone": header_row[71],
                            "fax": header_row[72],
                            "email": header_row[73]
                          },
                        "bill_to": {
                            "firstname": bill_to_first_name,
                            "lastname": bill_to_last_name,
                            "address1": header_row[76],
                            "address2": header_row[77],
                            "zipcode": header_row[78],
                            "city": header_row[79],
                            "state": header_row[80],
                            "country": header_row[81],
                            "phone": header_row[82],
                            "fax": header_row[83],
                            "email": header_row[84]
                        },
                        "rma": header_row[85],
                        "return_tracking_number": header_row[86],
                        "last_user": header_row[87],
                        "order_header_comments": header_row[88],
                        "items": []
                    }

                    data['receipts'].append(selected_receipt)

                selected_receipt['items'].append({
                    "record_type": row[0],
                    "line_number": row[1],
                    "item": row[2],
                    "item_description": row[3],
                    "lot_number": row[4],
                    "unit_of_measure": row[5],
                    "quantity_received": row[6],
                    "cube_received": row[7],
                    "quantity_received_in_good_condition": row[8],
                    "cube_of_product_received_in_good_condition": row[9],
                    "quantity_received_in_damaged_condition": row[10],
                    "quantity_ordered": row[11],
                    "item_weight": row[12],
                    "weight_qualifier": row[13],
                    "weight_uom": row[14],
                    "volume": row[15],
                    "volume_uom": row[16],
                    "detail_passthru_character_field_1": row[17],
                    "detail_passthru_character_field_2": row[18],
                    "detail_passthru_character_field_3": row[19],
                    "detail_passthru_character_field_4": row[20],
                    "detail_passthru_character_field_5": row[21],
                    "detail_passthru_character_field_6": row[22],
                    "detail_passthru_character_field_7": row[23],
                    "detail_passthru_character_field_8": row[24],
                    "detail_passthru_character_field_9": row[25],
                    "detail_passthru_character_field_10": row[26],
                    "detail_passthru_character_field_11": row[27],
                    "detail_passthru_character_field_12": row[28],
                    "detail_passthru_character_field_13": row[29],
                    "detail_passthru_character_field_14": row[30],
                    "detail_passthru_character_field_15": row[31],
                    "detail_passthru_character_field_16": row[32],
                    "detail_passthru_character_field_17": row[33],
                    "detail_passthru_character_field_18": row[34],
                    "detail_passthru_character_field_19": row[35],
                    "detail_passthru_character_field_20": row[36],
                    "detail_passthru_num_field_1": row[37],
                    "detail_passthru_num_field_2": row[38],
                    "detail_passthru_num_field_3": row[39],
                    "detail_passthru_num_field_4": row[40],
                    "detail_passthru_num_field_5": row[41],
                    "detail_passthru_num_field_6": row[42],
                    "detail_passthru_num_field_7": row[43],
                    "detail_passthru_num_field_8": row[44],
                    "detail_passthru_num_field_9": row[45],
                    "detail_passthru_num_field_10": row[46],
                    "detail_passthru_date_field_1": row[47],
                    "detail_passthru_date_field_2": row[48],
                    "detail_passthru_date_field_3": row[49],
                    "detail_passthru_date_field_4": row[50],
                    "detail_passthru_dollar_field_1": row[51],
                    "detail_passthru_dollar_field_2": row[52],
                    "quantity_on_hold": row[53],
                    "inventory_status_of_the_quantity_received": row[54],
                    "serial_number": row[55],
                    "user_item_1": row[56],
                    "user_item_2": row[57],
                    "user_item_3": row[58],
                    "original_line_number": row[59],
                    "unload_date": row[60],
                    "condition": row[61],
                    "inventory_class": row[62],
                    # "synapse_order_id": row[63] or "",
                    # "synapse_ship_id": row[64] or "",
                })
        s.close()

        return json.dumps(data)