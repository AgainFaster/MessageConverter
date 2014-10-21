from io import StringIO
from django.test import TestCase
import json
from .json2csv import Json2Csv
from .csv2json import Csv2Json
from .tasks import get_messages


class TestJson2Csv(TestCase):

    def test_init(self):
        outline = {'map': [['some_header', 'some_key']]}
        loader = Json2Csv(outline)
        self.assertIn('some_header', loader.key_map)

        self.assertRaises(ValueError, Json2Csv, None)

        self.assertRaises(ValueError, Json2Csv, {})

    def test_process_row(self):
        """Given a valid key-map and ddata, it should return a valid row"""
        outline = {'map': [['id', '_id'], ['count', 'count']]}
        loader = Json2Csv(outline)
        test_data = json.loads('{"_id" : "Someone","count" : 1}')
        row = loader.process_row(test_data)

        self.assertIs(type(row), dict)
        self.assertIn('id', row.keys())
        self.assertIn('count', row.keys())

        self.assertEquals(row['id'], 'Someone')
        self.assertEquals(row['count'], 1)

    def test_process_row_nested_data(self):
        """Ensure that nested keys (with . notation) are processed"""
        key_map = {"map": [['author', 'source.author'], ['message', 'message.original']]}
        loader = Json2Csv(key_map)
        test_data = json.loads(
            '{"source": {"author": "Someone"}, "message": {"original": "Hey!", "Revised": "Hey yo!"}}'
        )
        row = loader.process_row(test_data)

        self.assertIs(type(row), dict)
        self.assertIn('author', row.keys())
        self.assertIn('message', row.keys())

        self.assertEquals(row['author'], 'Someone')
        self.assertEquals(row['message'], 'Hey!')

    def test_process_row_array_index(self):
        """Ensure that array indices are properly handled as part of the dot notation"""
        pass

    # def test_process_each(self):
    #     outline = {'map': [['id', '_id'], ['count', 'count']], 'collection': 'result'}
    #     loader = Json2Csv(outline)
    #
    #     test_data = json.loads('{"result":[{"_id" : "Someone","count" : 1}]}')
    #     loader.process_each(test_data)
    #
    #     self.assertEquals(len(loader.rows), 1)
    #     row = loader.rows[0]
    #     self.assertIs(type(row), dict)
    #     self.assertIn('id', row.keys())
    #     self.assertIn('count', row.keys())
    #
    #     self.assertEquals(row['id'], 'Someone')
    #     self.assertEquals(row['count'], 1)

    # def test_process_each_optional_key(self):
    #     """Ensure a key that is not always present won't prevent data extraction
    #     Where the data is missing, None is returned
    #     """
    #     outline = {'map': [['id', '_id'], ['count', 'count']]}
    #     loader = Json2Csv(outline)
    #
    #     test_data = json.loads('[{"_id" : "Someone","count" : 1}, {"_id": "Another"}]')
    #     self.assertEquals(len(test_data), 2)
    #     loader.process_each(test_data)
    #
    #     self.assertEquals(len(loader.rows), 2)
    #     second_row = loader.rows[1]
    #     self.assertEquals(second_row['id'], 'Another')
    #     self.assertIsNone(second_row['count'])

    # def test_load_json(self):
    #     outline = {"map": [['author', 'source.author'], ['message', 'message.original']], "collection": "nodes"}
    #     loader = Json2Csv(outline)
    #     with open('fixtures/data.json') as f:
    #         loader.load(f)
    #
    #     first_row = loader.rows[0]
    #     self.assertEqual(first_row['author'], 'Someone')
    #     second_row = loader.rows[1]
    #     self.assertEqual(second_row['author'], 'Another')
    #     third_row = loader.rows[2]
    #     self.assertEqual(third_row['author'], 'Me too')

    # def test_load_bare_json(self):
    #     outline = {"map": [['author', 'source.author'], ['message', 'message.original']]}
    #     loader = Json2Csv(outline)
    #     with open('fixtures/bare_data.json') as f:
    #         loader.load(f)
    #
    #     first_row = loader.rows[0]
    #     self.assertEqual(first_row['author'], 'Someone')
    #     second_row = loader.rows[1]
    #     self.assertEqual(second_row['author'], 'Another')
    #     third_row = loader.rows[2]
    #     self.assertEqual(third_row['author'], 'Me too')

    def test_write_csv(self):
        pass


class TestCsv2Json(TestCase):

    def test_prefixed_outline(self):

        outline = {
            "collection": "inventory",
            "outline_per_type": "I",
            "outline":
                {
                    "type": "I.0",
                     "id": "I.1",
                     "total_quantity": "I.2",
                     "committed_quantity": "I.3",
                     "entered_quantity": "I.4",
                     "outline": {
                         "collection": "receipts",
                         "outline_per_type": "R",
                         "outline": {
                             "reference": "R.4",
                             "type": "R.0",
                             "sku": "R.1",
                             "i_sku": "I.1",
                             "receipt_total_quantity": "R.2",
                             "receipt_scheduled_date": "R.3"
                         }
                     }
                }
        }

        csv2json = Csv2Json(outline)

        csv_str = """I,[I0 SKU],[I0 total quantity],[I0 committed quantity],[I0 entered quantity]
R,[I0 R0 SKU],[I0 R0 total quantity],[I0 R0 date],[I0 R0 Reference]
R,[I0 R1 SKU],[I0 R1 total quantity],[I0 R1 date],[I0 R1 Reference]
I,[I1 SKU],[I1 total quantity],[I1 committed quantity],[I1 entered quantity]
R,[I1 R0 SKU],[I1 R0 total quantity],[I1 R0 date],[I1 R0 Reference]
R,[I1 R1 SKU],,[I1 R1 date]"""

        json_data = csv2json.convert(csv_str)

        data = json.loads(json_data)

        self.assertTrue('inventory' in data)
        self.assertTrue(isinstance(data['inventory'], list))
        self.assertEqual(len(data['inventory']), 2)

        self.assertEqual(data['inventory'][0].get('type'), 'I')
        self.assertEqual(data['inventory'][0].get('id'), '[I0 SKU]')
        self.assertEqual(data['inventory'][0].get('total_quantity'), '[I0 total quantity]')
        self.assertEqual(data['inventory'][0].get('committed_quantity'), '[I0 committed quantity]')
        self.assertEqual(data['inventory'][0].get('entered_quantity'), '[I0 entered quantity]')

        receipts = data['inventory'][0].get('receipts')
        self.assertTrue(isinstance(receipts, list))
        self.assertEqual(len(receipts), 2)
        self.assertEqual(receipts[0].get('type'), 'R')
        self.assertEqual(receipts[0].get('reference'), '[I0 R0 Reference]')
        self.assertEqual(receipts[0].get('sku'), '[I0 R0 SKU]')
        self.assertEqual(receipts[0].get('i_sku'), '[I0 SKU]')
        self.assertEqual(receipts[0].get('receipt_total_quantity'), '[I0 R0 total quantity]')
        self.assertEqual(receipts[0].get('receipt_scheduled_date'), '[I0 R0 date]')
        self.assertEqual(receipts[1].get('type'), 'R')
        self.assertEqual(receipts[1].get('reference'), '[I0 R1 Reference]')
        self.assertEqual(receipts[1].get('sku'), '[I0 R1 SKU]')
        self.assertEqual(receipts[1].get('i_sku'), '[I0 SKU]')
        self.assertEqual(receipts[1].get('receipt_total_quantity'), '[I0 R1 total quantity]')
        self.assertEqual(receipts[1].get('receipt_scheduled_date'), '[I0 R1 date]')

        self.assertEqual(data['inventory'][1].get('type'), 'I')
        self.assertEqual(data['inventory'][1].get('id'), '[I1 SKU]')
        self.assertEqual(data['inventory'][1].get('total_quantity'), '[I1 total quantity]')
        self.assertEqual(data['inventory'][1].get('committed_quantity'), '[I1 committed quantity]')
        self.assertEqual(data['inventory'][1].get('entered_quantity'), '[I1 entered quantity]')

        receipts = data['inventory'][1].get('receipts')
        self.assertTrue(isinstance(receipts, list))
        self.assertEqual(len(receipts), 2)
        self.assertEqual(receipts[0].get('type'), 'R')
        self.assertEqual(receipts[0].get('reference'), '[I1 R0 Reference]')
        self.assertEqual(receipts[0].get('sku'), '[I1 R0 SKU]')
        self.assertEqual(receipts[0].get('i_sku'), '[I1 SKU]')
        self.assertEqual(receipts[0].get('receipt_total_quantity'), '[I1 R0 total quantity]')
        self.assertEqual(receipts[0].get('receipt_scheduled_date'), '[I1 R0 date]')
        self.assertEqual(receipts[1].get('type'), 'R')
        self.assertEqual(receipts[1].get('reference'), None)
        self.assertEqual(receipts[1].get('sku'), '[I1 R1 SKU]')
        self.assertEqual(receipts[1].get('i_sku'), '[I1 SKU]')
        self.assertEqual(receipts[1].get('receipt_total_quantity'), '')
        self.assertEqual(receipts[1].get('receipt_scheduled_date'), '[I1 R1 date]')


    def test_non_prefixed_outline(self):
        outline = {
            "collection": "orderstatus",
            "outline": {"id": "0", "status": "1"}
        }

        csv2json = Csv2Json(outline)
        csv_str = """12345,6
54321,7"""

        json_data = csv2json.convert(csv_str)
        data = json.loads(json_data)

        self.assertTrue('orderstatus' in data)
        self.assertTrue(isinstance(data['orderstatus'], list))
        self.assertEqual(len(data['orderstatus']), 2)

        self.assertEqual(data['orderstatus'][0].get('id'), '12345')
        self.assertEqual(data['orderstatus'][0].get('status'), '6')
        self.assertEqual(data['orderstatus'][1].get('id'), '54321')
        self.assertEqual(data['orderstatus'][1].get('status'), '7')

class TestTasks(TestCase):
    def test_get_messages(self):

        converted_message = json.dumps({"orderstatus": [
            {"id": "0", "status": "4"},
            {"id": "1", "status": "3"},
            {"id": "2", "status": "2"},
            {"id": "3", "status": "1"},
            {"id": "4", "status": "0"}
        ]})

        messages_per_delivery = 2
        messages = get_messages(converted_message, messages_per_delivery)

        self.assertEqual(len(messages), 3)

        chunk0 = json.loads(messages[0])['orderstatus']
        chunk1 = json.loads(messages[1])['orderstatus']
        chunk2 = json.loads(messages[2])['orderstatus']

        self.assertEqual(len(chunk0), 2)
        self.assertEqual(len(chunk1), 2)
        self.assertEqual(len(chunk2), 1)

        self.assertEqual(chunk0[0]['id'], "0")
        self.assertEqual(chunk0[0]['status'], "4")
        self.assertEqual(chunk0[1]['id'], "1")
        self.assertEqual(chunk0[1]['status'], "3")

        self.assertEqual(chunk1[0]['id'], "2")
        self.assertEqual(chunk1[0]['status'], "2")
        self.assertEqual(chunk1[1]['id'], "3")
        self.assertEqual(chunk1[1]['status'], "1")

        self.assertEqual(chunk2[0]['id'], "4")
        self.assertEqual(chunk2[0]['status'], "0")

        messages_per_delivery = 0
        messages = get_messages(converted_message, messages_per_delivery)
        self.assertEqual(len(messages), 1)



