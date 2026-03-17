[![PyPI version](https://img.shields.io/pypi/v/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI downloads](https://img.shields.io/pypi/dm/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI license](https://img.shields.io/pypi/l/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![GitHub stars](https://img.shields.io/github/stars/MrDebugger/bs2json.svg)](https://github.com/MrDebugger/bs2json/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/MrDebugger/bs2json.svg)](https://github.com/MrDebugger/bs2json/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/MrDebugger/bs2json.svg)](https://github.com/MrDebugger/bs2json/commits)

# bs2json

A lightweight Python library that converts BeautifulSoup4 HTML elements into structured JSON. Parse any HTML and get clean, traversable dictionaries — with full control over element ordering, comments, whitespace, and label naming.

## Installation

```bash
pip install -U bs2json
```

**Requirements:** Python 3.8+ | Only dependency: `beautifulsoup4`

## Quick Start

```python
from bs2json import BS2Json

html = """
<html>
<head><title>My Page</title></head>
<body>
    <h1>Welcome</h1>
    <p class="intro">Hello <b>world</b></p>
    <a href="/link1">Link 1</a>
    <a href="/link2">Link 2</a>
</body>
</html>
"""

converter = BS2Json(html)
result = converter.convert()
converter.prettify()
```

**Output:**
```python
{'html': {'head': {'title': 'My Page'},
          'body': {'h1': 'Welcome',
                   'p': {'attrs': {'class': ['intro']},
                         'text': 'Hello',
                         'b': 'world'},
                   'a': [{'attrs': {'href': '/link1'}, 'text': 'Link 1'},
                         {'attrs': {'href': '/link2'}, 'text': 'Link 2'}]}}}
```

## Features

### Convert Specific Tags

```python
converter = BS2Json(html)

# By tag name
converter.convert('body')
# {'body': {'h1': 'Welcome', 'p': {...}, 'a': [...]}}

# By CSS class
converter.convert(class_='intro')
# {'p': {'attrs': {'class': ['intro']}, 'text': 'Hello', 'b': 'world'}}

# By id or any bs4 find() argument
converter.convert('a', href='/link1')
# {'a': {'attrs': {'href': '/link1'}, 'text': 'Link 1'}}
```

### Convert Multiple Tags

```python
converter = BS2Json(html)

# As a list of individual results
converter.convert_all('a')
# [{'a': {'attrs': {'href': '/link1'}, 'text': 'Link 1'}},
#  {'a': {'attrs': {'href': '/link2'}, 'text': 'Link 2'}}]

# Grouped by tag name into a single dict
converter.convert_all('a', join=True)
# [{'a': [{'attrs': {'href': '/link1'}, 'text': 'Link 1'},
#         {'attrs': {'href': '/link2'}, 'text': 'Link 2'}]}]
```

### Preserve Element Order

By default, sibling elements with the same tag are grouped together. Use `keep_order=True` to preserve the original document order — useful when the sequence of elements matters:

```python
html = '<html><body><h3>First</h3><p>Text</p><h3>Second</h3></body></html>'

# Default: groups by tag name
BS2Json(html).convert()
# {'html': {'body': {'h3': ['First', 'Second'], 'p': 'Text'}}}

# Ordered: preserves document order
BS2Json(html, keep_order=True).convert()
# {'html': [{'body': [{'h3': 'First'}, {'p': 'Text'}, {'h3': 'Second'}]}]}
```

### Control Comments and Whitespace

```python
comment_html = '<html><body><!-- TODO: fix --><p>  hello  </p></body></html>'

# Include comments (default)
BS2Json(comment_html).convert()
# {'html': {'body': {'comment': '<!-- TODO: fix -->', 'p': 'hello'}}}

# Exclude comments
BS2Json(comment_html, include_comments=False).convert()
# {'html': {'body': {'p': 'hello'}}}

# Preserve whitespace (stripped by default)
BS2Json(comment_html, strip=False).convert()
# {'html': {'body': {'comment': '<!-- TODO: fix -->', 'p': '  hello  '}}}
```

### Custom Labels

Change the JSON key names for attributes, text content, and comments:

```python
converter = BS2Json('<html><body><p class="x">hello</p></body></html>')
converter.labels(attrs='attributes', text='content', comment='notes')
result = converter.convert()
# {'html': {'body': {'p': {'attributes': {'class': ['x']}, 'content': 'hello'}}}}
```

### Save and Prettify

```python
converter = BS2Json(html)
converter.convert()

# Save to JSON file
converter.save('output.json')

# Save with custom formatting
converter.save('compact.json', prettify=False)
converter.save('indented.json', indent=2)

# Save to a file-like object
import io
buf = io.StringIO()
converter.save(buf)

# Pretty-print to stdout
converter.prettify()
```

### Context Manager and Callable

```python
# Use as context manager
with BS2Json(html) as converter:
    result = converter.convert()

# Use as callable (shortcut for .convert())
converter = BS2Json(html)
result = converter()
```

### Extension Mode

Monkey-patch `.to_json()` directly onto every BeautifulSoup Tag element:

```python
from bs4 import BeautifulSoup
from bs2json import install, remove

install()

soup = BeautifulSoup(html, 'html.parser')

# Now every tag has .to_json()
soup.find('body').to_json()
soup.body.to_json(keep_order=True)
soup.find('a').to_json(include_comments=False, strip=False)

remove()  # clean up when done
```

### Configuration Object

All conversion options are stored in a `ConversionConfig` dataclass, accessible and modifiable at any time:

```python
from bs2json import BS2Json, ConversionConfig

converter = BS2Json(html, keep_order=True, strip=False)
print(converter.config)
# ConversionConfig(attr_name='attrs', text_name='text', comment_name='comment',
#                  include_comments=True, strip=False, keep_order=True)

# Modify config directly
converter.config.keep_order = False
converter.config.include_comments = False
```

## Also Works With BeautifulSoup Objects

You can pass an existing BeautifulSoup object or Tag instead of a raw HTML string:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# From a soup object
BS2Json(soup).convert()

# From a specific tag
tag = soup.find('body')
BS2Json(tag).convert()

# Convert on-the-fly with no soup
converter = BS2Json()
converter.convert(tag)
```

## API Reference

### `BS2Json`

| Method | Description |
|--------|-------------|
| `BS2Json(soup, features, *, include_comments, strip, keep_order, **kwargs)` | Initialize from HTML string, Tag, or BeautifulSoup object |
| `.convert(element=None, json=None, *, inplace=False, **kwargs)` | Convert a single tag to a dict |
| `.convert_all(elements=None, lst=None, *, join=False, **kwargs)` | Convert multiple tags to a list of dicts |
| `.labels(attrs=..., text=..., comment=...)` | Change JSON key names |
| `.save(file, /, mode='w', *, prettify=True, indent=4)` | Save last result to file path or file object |
| `.prettify()` | Pretty-print last result to stdout |
| `.config` | `ConversionConfig` dataclass with all options |
| `.last_obj` | Result of the most recent conversion |
| `.soup` | The underlying BeautifulSoup object |

### `ConversionConfig`

| Field | Default | Description |
|-------|---------|-------------|
| `attr_name` | `"attrs"` | JSON key for element attributes |
| `text_name` | `"text"` | JSON key for text content |
| `comment_name` | `"comment"` | JSON key for HTML comments |
| `include_comments` | `True` | Whether to include HTML comments |
| `strip` | `True` | Strip leading/trailing whitespace from text |
| `keep_order` | `False` | Preserve element order instead of grouping |

## Contributing

We appreciate all contributions. If you are planning to contribute bug-fixes, please do so without further discussion.

If you plan to contribute new features, please first open an issue and discuss the feature with us.

<a href="https://github.com/MrDebugger/bs2json/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MrDebugger/bs2json"/>
</a>
