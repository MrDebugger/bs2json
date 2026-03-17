import unittest
import io
import sys
import os
import contextlib
sys.path.insert(0, os.path.dirname(__file__))
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

    def test_convert_all_no_args_crashes(self):
        """convert_all() with no args should not crash when soup is set."""
        bs2json = BS2Json(self.html_str)
        # This triggers the bug: self.soup (BeautifulSoup) fails isinstance(ResultSet)
        try:
            result = bs2json.convert_all()
        except TypeError as e:
            if 'ResultSet' in str(e):
                self.fail("convert_all() crashed with ResultSet TypeError — bug not fixed")
            raise
        self.assertIsInstance(result, list)

    def test_convert_all_with_string(self):
        """convert_all('a') should find and convert all matching tags."""
        bs2json = BS2Json(self.html_str)
        result = bs2json.convert_all('a')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    def test_instance_isolation(self):
        """Two instances must not share mutable state."""
        a = BS2Json(self.html_str)
        b = BS2Json('<html><body><p>hello</p></body></html>')
        b.labels(text="txt")
        a.convert()
        # a should still use default label "text", not "txt"
        body = a.last_obj['html']['body']
        # The bug: b.labels(text="txt") corrupts a's labels because __labels is shared.
        # With the bug, the second <p> will have 'txt' key instead of 'text'.
        story_p = body['p']
        if isinstance(story_p, list):
            for p in story_p:
                if isinstance(p, dict):
                    self.assertNotIn('txt', p, "Label 'text' was corrupted to 'txt' by another instance")

if __name__ == "__main__":
    unittest.main()