[![PyPI version](https://img.shields.io/pypi/v/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI downloads](https://img.shields.io/pypi/dm/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI license](https://img.shields.io/pypi/l/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![GitHub stars](https://img.shields.io/github/stars/MrDebugger/bs2json.svg)](https://github.com/MrDebugger/bs2json/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/MrDebugger/bs2json.svg)](https://github.com/MrDebugger/bs2json/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/MrDebugger/bs2json.svg)](https://github.com/MrDebugger/bs2json/commits)

# bs2json

A lightweight Python library that converts BeautifulSoup4 HTML elements into structured JSON. Parse any HTML and get clean, traversable dictionaries — preserving document order, with full control over comments, whitespace, and label naming.

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
          'body': {'children': [{'h1': 'Welcome'},
                                {'p': {'attrs': {'class': ['intro']},
                                       'children': [{'text': 'Hello'},
                                                    {'b': 'world'}]}},
                                {'a': {'attrs': {'href': '/link1'},
                                       'text': 'Link 1'}},
                                {'a': {'attrs': {'href': '/link2'},
                                       'text': 'Link 2'}}]}}}
```

Elements preserve their original document order. Single text children stay simple (`{'h1': 'Welcome'}`), while multiple children use `{'children': [...]}`.

## Features

### Convert Specific Tags

```python
converter = BS2Json(html)

# By tag name
converter.convert('body')

# By CSS class
converter.convert(class_='intro')

# By attribute
converter.convert('a', href='/link1')
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
```

### Group by Tag Name (Legacy Mode)

By default, elements preserve document order. Use `group_by_tag=True` to group siblings by tag name — useful when you don't care about order and want quick access by tag:

```python
html = '<html><body><h3>First</h3><p>Text</p><h3>Second</h3></body></html>'

# Default: preserves document order
BS2Json(html).convert()
# {'html': {'body': {'children': [{'h3': 'First'}, {'p': 'Text'}, {'h3': 'Second'}]}}}

# Grouped: siblings merged by tag name
BS2Json(html, group_by_tag=True).convert()
# {'html': {'body': {'h3': ['First', 'Second'], 'p': 'Text'}}}
```

### Control Comments and Whitespace

```python
comment_html = '<html><body><!-- TODO: fix --><p>  hello  </p></body></html>'

# Include comments (default)
BS2Json(comment_html).convert()

# Exclude comments
BS2Json(comment_html, include_comments=False).convert()

# Preserve whitespace (stripped by default)
BS2Json(comment_html, strip=False).convert()
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
soup.find('a').to_json(include_comments=False, strip=False)

remove()  # clean up when done
```

### Configuration Object

All conversion options are stored in a `ConversionConfig` dataclass, accessible and modifiable at any time:

```python
from bs2json import BS2Json, ConversionConfig

converter = BS2Json(html, strip=False)
print(converter.config)
# ConversionConfig(attr_name='attrs', text_name='text', comment_name='comment',
#                  include_comments=True, strip=False, group_by_tag=False)

# Modify config directly
converter.config.group_by_tag = True
converter.config.include_comments = False
```

## Also Works With BeautifulSoup Objects

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
| `BS2Json(soup, features, *, include_comments, strip, group_by_tag, **kwargs)` | Initialize from HTML string, Tag, or BeautifulSoup object |
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
| `group_by_tag` | `False` | Group siblings by tag name instead of preserving order |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, versioning guide, and how to submit changes.

<a href="https://github.com/MrDebugger/bs2json/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MrDebugger/bs2json"/>
</a>
