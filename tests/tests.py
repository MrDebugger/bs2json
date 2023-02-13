import unittest
import io
import sys
import contextlib
from bs4 import BeautifulSoup
from bs2json import BS2Json
from expected_output import input_1, expected_1, expected_2, expected_3, expected_4


@contextlib.contextmanager
def capture_output():
    output = {}
    try:
        # Redirect
        sys.stdout = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
        sys.stderr = io.TextIOWrapper(io.BytesIO(), sys.stderr.encoding)
        yield output
    finally:
        # Read
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        output['stdout'] = sys.stdout.read()
        output['stderr'] = sys.stderr.read()
        sys.stdout.close()
        sys.stderr.close()

        # Restore
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


class TestBS2Json(unittest.TestCase):
    def setUp(self):
        self.html_str = input_1
        self.soup = BeautifulSoup(self.html_str, features='html.parser')

    def test_initialize(self):
        bs2json = BS2Json(self.soup)
        self.assertIsInstance(bs2json.soup, BeautifulSoup)
        
        bs2json = BS2Json(self.html_str)
        self.assertIsInstance(bs2json.soup, BeautifulSoup)
        
        bs2json = BS2Json(soup=None)
        self.assertIsNone(bs2json.soup)
    
    def test_default(self):
        bs2json = BS2Json()
        bs2json.convert(self.soup)
        self.assertEqual(bs2json.last_obj, expected_1)

    def test_soup(self):
        bs2json = BS2Json(self.soup)
        bs2json.convert('body')
        self.assertEqual(bs2json.last_obj, {'body':expected_1['html']['body']})

    def test_nojoin(self):
        bs2json = BS2Json(self.html_str)
        bs2json.convert_all(class_='sister')
        self.assertEqual(bs2json.last_obj, expected_2)
    
    def test_join(self):
        bs2json = BS2Json(self.html_str)
        bs2json.convert_all(class_='sister', join=True)
        self.assertEqual(bs2json.last_obj, expected_3)

    def test_prettify(self):
        bs2json = BS2Json(self.html_str)
        bs2json.convert()
        with capture_output() as out:
            bs2json.prettify()
        result = out['stdout']
        self.assertEqual(result, expected_4)

if __name__ == "__main__":
    unittest.main()