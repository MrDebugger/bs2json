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

    # --- Initialization ---

    def test_initialize(self):
        bs2json = BS2Json(self.soup)
        self.assertIsInstance(bs2json.soup, BeautifulSoup)

        bs2json = BS2Json(self.html_str)
        self.assertIsInstance(bs2json.soup, BeautifulSoup)

        bs2json = BS2Json(soup=None)
        self.assertIsNone(bs2json.soup)

    def test_instance_isolation(self):
        """Two instances must not share mutable state."""
        a = BS2Json(self.html_str, group_by_tag=True)
        b = BS2Json('<html><body><p>hello</p></body></html>', group_by_tag=True)
        b.labels(text="txt")
        a.convert()
        body = a.last_obj['html']['body']
        story_p = body['p']
        if isinstance(story_p, list):
            for p in story_p:
                if isinstance(p, dict):
                    self.assertNotIn('txt', p, "Label 'text' was corrupted to 'txt' by another instance")

    def test_repr(self):
        """BS2Json should have a useful repr."""
        converter = BS2Json(self.html_str)
        r = repr(converter)
        self.assertIn('BS2Json', r)

    def test_context_manager(self):
        """BS2Json should work as a context manager."""
        with BS2Json(self.html_str, group_by_tag=True) as converter:
            result = converter.convert()
        self.assertEqual(result, expected_1)

    def test_callable(self):
        """BS2Json instance should be callable via __call__."""
        converter = BS2Json(self.html_str, group_by_tag=True)
        result = converter()
        self.assertEqual(result, expected_1)

    # --- Default mode (ordered, preserves document order) ---

    def test_default_ordered(self):
        """Default mode preserves element order."""
        html = '<html><body><h3>first</h3><p>paragraph</p><h3>second</h3></body></html>'
        result = BS2Json(html).convert()
        body_content = result['html']['body']['children']
        self.assertIsInstance(body_content, list)
        tag_names = [list(el.keys())[0] for el in body_content]
        self.assertEqual(tag_names, ['h3', 'p', 'h3'])
        self.assertEqual(body_content[0]['h3'], 'first')
        self.assertEqual(body_content[1]['p'], 'paragraph')
        self.assertEqual(body_content[2]['h3'], 'second')

    def test_ordered_attrs_with_children(self):
        """Elements with attrs produce {attrs, children} or {attrs, tag}."""
        html = '<html><body><table id="t1"><tr><td>a</td></tr></table></body></html>'
        result = BS2Json(html).convert()
        table = result['html']['body']['table']
        self.assertIsInstance(table, dict)
        self.assertIn('attrs', table)
        self.assertEqual(table['attrs']['id'], 't1')

    def test_ordered_multiple_children(self):
        """Multiple children use {children: [...]}."""
        html = '<html><body><table><tr><td>a</td><td>b</td></tr></table></body></html>'
        result = BS2Json(html).convert()
        tr = result['html']['body']['table']['tr']
        self.assertIsInstance(tr, dict)
        self.assertIn('children', tr)
        self.assertEqual(len(tr['children']), 2)

    def test_ordered_simple_text(self):
        """Single text child stays unwrapped."""
        html = '<html><body><h1>hello</h1></body></html>'
        result = BS2Json(html).convert()
        self.assertEqual(result['html']['body']['h1'], 'hello')

    def test_ordered_mixed_content(self):
        """Mixed text and tags use children list."""
        html = '<html><body><p>hello <b>world</b></p></body></html>'
        result = BS2Json(html).convert()
        p = result['html']['body']['p']
        self.assertIn('children', p)
        self.assertEqual(len(p['children']), 2)

    # --- group_by_tag mode (legacy, groups siblings by tag name) ---

    def test_group_by_tag(self):
        """group_by_tag=True groups siblings by tag name."""
        bs2json = BS2Json(group_by_tag=True)
        bs2json.convert(self.soup)
        self.assertEqual(bs2json.last_obj, expected_1)

    def test_group_by_tag_find(self):
        """group_by_tag with find by tag name."""
        bs2json = BS2Json(self.soup, group_by_tag=True)
        bs2json.convert('body')
        self.assertEqual(bs2json.last_obj, {'body': expected_1['html']['body']})

    def test_group_by_tag_nojoin(self):
        bs2json = BS2Json(self.html_str, group_by_tag=True)
        bs2json.convert_all(class_='sister')
        self.assertEqual(bs2json.last_obj, expected_2)

    def test_group_by_tag_join(self):
        bs2json = BS2Json(self.html_str, group_by_tag=True)
        bs2json.convert_all(class_='sister', join=True)
        self.assertEqual(bs2json.last_obj, expected_3)

    def test_group_by_tag_prettify(self):
        bs2json = BS2Json(self.html_str, group_by_tag=True)
        bs2json.convert()
        with capture_output() as out:
            bs2json.prettify()
        result = out['stdout']
        self.assertEqual(result, expected_4)

    def test_group_by_tag_groups_same_tags(self):
        """group_by_tag groups duplicate tag names into lists."""
        html = '<html><body><h3>first</h3><p>paragraph</p><h3>second</h3></body></html>'
        result = BS2Json(html, group_by_tag=True).convert()
        body = result['html']['body']
        self.assertEqual(body['h3'], ['first', 'second'])

    # --- convert_all ---

    def test_convert_all_no_args(self):
        """convert_all() with no args should not crash when soup is set."""
        bs2json = BS2Json(self.html_str)
        try:
            result = bs2json.convert_all()
        except TypeError as e:
            if 'ResultSet' in str(e):
                self.fail("convert_all() crashed with ResultSet TypeError")
            raise
        self.assertIsInstance(result, list)

    def test_convert_all_with_string(self):
        """convert_all('a') should find and convert all matching tags."""
        bs2json = BS2Json(self.html_str)
        result = bs2json.convert_all('a')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    # --- Options ---

    def test_custom_labels(self):
        """labels() should change JSON key names."""
        bs2json = BS2Json('<html><body><p class="x">hello</p></body></html>')
        bs2json.labels(attrs='attributes', text='content')
        result = bs2json.convert()
        p = result['html']['body']['p']
        self.assertIn('attributes', p)
        self.assertNotIn('attrs', p)

    def test_include_comments_true(self):
        """include_comments=True should include HTML comments."""
        html = '<html><body><!-- a comment --><p>text</p></body></html>'
        result = BS2Json(html, include_comments=True).convert()
        body = result['html']['body']
        # Check comments appear somewhere in the output
        import json
        output = json.dumps(body)
        self.assertIn('comment', output)

    def test_include_comments_false(self):
        """include_comments=False should exclude HTML comments entirely."""
        html = '<html><body><!-- a comment --><p>text</p></body></html>'
        result = BS2Json(html, include_comments=False).convert()
        import json
        output = json.dumps(result)
        self.assertNotIn('comment', output)

    def test_strip_false(self):
        """strip=False should preserve whitespace."""
        html = '<html><body><p>  hello  </p></body></html>'
        result_strip = BS2Json(html, strip=True).convert()
        result_nostrip = BS2Json(html, strip=False).convert()
        self.assertEqual(result_strip['html']['body']['p'], 'hello')
        self.assertEqual(result_nostrip['html']['body']['p'], '  hello  ')

    # --- Save ---

    def test_save_to_file(self):
        """save() should write JSON to a file."""
        import tempfile, json, os
        bs2json = BS2Json(self.html_str, group_by_tag=True)
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
        bs2json = BS2Json(self.html_str, group_by_tag=True)
        bs2json.convert()
        buf = io.StringIO()
        bs2json.save(buf)
        buf.seek(0)
        data = json.load(buf)
        self.assertEqual(data, expected_1)

    # --- Extension ---

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

    # --- Error cases ---

    def test_convert_invalid_json_arg(self):
        """convert() should raise TypeError for non-dict json arg."""
        converter = BS2Json(self.html_str)
        with self.assertRaises(TypeError):
            converter.convert(json=[])

    def test_convert_all_invalid_lst_arg(self):
        """convert_all() should raise TypeError for non-list lst arg."""
        converter = BS2Json(self.html_str)
        with self.assertRaises(TypeError):
            converter.convert_all('a', lst={'key': 'val'})


if __name__ == "__main__":
    unittest.main()
