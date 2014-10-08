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
    def test_dict_outline(self):
        outline = {
            "collection": "inventory",
            "outline": {
                "I": ["type", "id", "total_quantity", "committed_quantity", "entered_quantity"],
                "R": ["type", "id", "receipt_total_quantity", "receipt_scheduled_date"]
            }
        }

        csv2json = Csv2Json(outline)

        csv_str = """I,[Item SKU],[total quantity],[committed quantity],[entered quantity]
R,[Item SKU],[total quantity],[date]"""

        json_data = csv2json.convert(csv_str)

        data = json.loads(json_data)
        self.assertTrue('inventory' in data)
        self.assertTrue(isinstance(data['inventory'], list))
        self.assertEqual(len(data['inventory']), 2)

        self.assertEqual(data['inventory'][0].get('type'), 'I')
        self.assertEqual(data['inventory'][0].get('id'), '[Item SKU]')
        self.assertEqual(data['inventory'][0].get('total_quantity'), '[total quantity]')
        self.assertEqual(data['inventory'][0].get('committed_quantity'), '[committed quantity]')
        self.assertEqual(data['inventory'][0].get('entered_quantity'), '[entered quantity]')

        self.assertEqual(data['inventory'][1].get('type'), 'R')
        self.assertEqual(data['inventory'][1].get('id'), '[Item SKU]')
        self.assertEqual(data['inventory'][1].get('receipt_total_quantity'), '[total quantity]')
        self.assertEqual(data['inventory'][1].get('receipt_scheduled_date'), '[date]')


    def test_list_outline(self):
        outline = {
            "collection": "orderstatus",
            "outline": ["id", "status"]
        }

        csv2json = Csv2Json(outline)
        csv_str = "12345,6"

        json_data = csv2json.convert(csv_str)
        data = json.loads(json_data)

        self.assertTrue('orderstatus' in data)
        self.assertTrue(isinstance(data['orderstatus'], list))
        self.assertEqual(len(data['orderstatus']), 1)

        self.assertEqual(data['orderstatus'][0].get('id'), '12345')
        self.assertEqual(data['orderstatus'][0].get('status'), '6')

class TestTasks(TestCase):
    def test_get_messages(self):
        r = StringIO('line0\nline1\nline2\nline3\nline4\n')

        # test without lines_per_message
        messages = get_messages(r)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], r.getvalue())

        # test lines_per_message greater than actual number of lines
        messages = get_messages(r, 100)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], r.getvalue())

        # test lines_per_message less than actual number of lines, and not dividing evenly
        messages = get_messages(r, 2)
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0], 'line0\nline1\n')
        self.assertEqual(messages[1], 'line2\nline3\n')
        self.assertEqual(messages[2], 'line4\n')

