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

    def test_save_to_file(self):
        """save() should write JSON to a file."""
        import tempfile, json, os
        bs2json = BS2Json(self.html_str)
        bs2json.convert()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmppath = f.name
        try:
            bs2json.save(tmppath)
            with open(tmppath) as f:
                data = json.load(f)
            self.assertEqual(data, expected_1)
        finally:
            os.unlink(tmppath)

    def test_save_to_file_object(self):
        """save() should write JSON to a file-like object."""
        import io, json
        bs2json = BS2Json(self.html_str)
        bs2json.convert()
        buf = io.StringIO()
        bs2json.save(buf)
        buf.seek(0)
        data = json.load(buf)
        self.assertEqual(data, expected_1)

    def test_custom_labels(self):
        """labels() should change JSON key names."""
        bs2json = BS2Json('<html><body><p class="x">hello</p></body></html>')
        bs2json.labels(attrs='attributes', text='content')
        result = bs2json.convert()
        p = result['html']['body']['p']
        self.assertIn('attributes', p)
        self.assertNotIn('attrs', p)

    def test_include_comments_true(self):
        """include_comments=True should include HTML comments with 'comment' key."""
        html = '<html><body><!-- a comment --><p>text</p></body></html>'
        bs2json = BS2Json(html, include_comments=True)
        result = bs2json.convert()
        body = result['html']['body']
        self.assertIn('comment', body)

    def test_include_comments_false(self):
        """include_comments=False should exclude HTML comments entirely."""
        html = '<html><body><!-- a comment --><p>text</p></body></html>'
        bs2json = BS2Json(html, include_comments=False)
        result = bs2json.convert()
        body = result['html']['body']
        self.assertNotIn('comment', body)
        self.assertEqual(body['p'], 'text')

    def test_strip_false(self):
        """strip=False should preserve whitespace."""
        html = '<html><body><p>  hello  </p></body></html>'
        result_strip = BS2Json(html, strip=True).convert()
        result_nostrip = BS2Json(html, strip=False).convert()
        self.assertEqual(result_strip['html']['body']['p'], 'hello')
        self.assertEqual(result_nostrip['html']['body']['p'], '  hello  ')

    def test_context_manager(self):
        """BS2Json should work as a context manager."""
        with BS2Json(self.html_str) as converter:
            result = converter.convert()
        self.assertEqual(result, expected_1)

    def test_callable(self):
        """BS2Json instance should be callable via __call__."""
        converter = BS2Json(self.html_str)
        result = converter()
        self.assertEqual(result, expected_1)

    def test_extension_install_remove(self):
        """install() should add to_json to Tag, remove() should remove it."""
        from bs2json import install, remove
        from bs4 import element
        try:
            install()
            self.assertTrue(hasattr(element.Tag, 'to_json'))
        finally:
            remove()
        self.assertFalse(hasattr(element.Tag, 'to_json'))

    def test_convert_invalid_json_arg(self):
        """convert() should raise TypeError for non-dict json arg."""
        converter = BS2Json(self.html_str)
        with self.assertRaises(TypeError):
            converter.convert(json=[])

    def test_convert_all_invalid_lst_arg(self):
        """convert_all() should raise TypeError for non-list lst arg.

        Note: an empty dict {} is falsy and gets replaced by [] before the type
        check, so a non-empty dict is used here to actually trigger the TypeError.
        """
        converter = BS2Json(self.html_str)
        with self.assertRaises(TypeError):
            converter.convert_all('a', lst={'key': 'val'})

    def test_keep_order(self):
        """keep_order=True should preserve element order instead of grouping."""
        html = '<html><body><h3>first</h3><p>paragraph</p><h3>second</h3></body></html>'
        bs2json = BS2Json(html, keep_order=True)
        result = bs2json.convert()
        # With keep_order, children are ordered lists instead of grouped dicts.
        # Navigate to body content.
        html_content = result['html']
        self.assertIsInstance(html_content, list)
        # Find the body entry
        body_content = None
        for item in html_content:
            if isinstance(item, dict) and 'body' in item:
                body_content = item['body']
                break
        self.assertIsNotNone(body_content, "Could not find 'body' in html children list")
        self.assertIsInstance(body_content, list)
        # Order should be: h3, p, h3
        tag_names = [list(el.keys())[0] for el in body_content]
        self.assertEqual(tag_names, ['h3', 'p', 'h3'])
        self.assertEqual(body_content[0]['h3'], 'first')
        self.assertEqual(body_content[1]['p'], 'paragraph')
        self.assertEqual(body_content[2]['h3'], 'second')

    def test_repr(self):
        """BS2Json should have a useful repr."""
        converter = BS2Json(self.html_str)
        r = repr(converter)
        self.assertIn('BS2Json', r)

    def test_keep_order_attrs_with_children(self):
        """keep_order: elements with attrs should use {attrs, children} not append."""
        html = '<html><body><table id="t1"><tr><td>a</td></tr></table></body></html>'
        result = BS2Json(html, keep_order=True).convert()
        html_content = result['html']
        body = None
        for item in html_content:
            if isinstance(item, dict) and 'body' in item:
                body = item['body']
                break
        table_entry = body[0]
        table = table_entry['table']
        # Should be a dict with attrs and children, not a list
        self.assertIsInstance(table, dict)
        self.assertIn('attrs', table)
        self.assertEqual(table['attrs']['id'], 't1')
        self.assertIn('children', table)
        self.assertIsInstance(table['children'], list)

    def test_keep_order_default_off(self):
        """Default behavior (keep_order=False) should still group by tag name."""
        html = '<html><body><h3>first</h3><p>paragraph</p><h3>second</h3></body></html>'
        bs2json = BS2Json(html)
        result = bs2json.convert()
        body = result['html']['body']
        # h3 should be grouped into a list
        self.assertEqual(body['h3'], ['first', 'second'])


if __name__ == "__main__":
    unittest.main()