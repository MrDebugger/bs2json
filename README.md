[![PyPI version](https://img.shields.io/pypi/v/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPI license](https://img.shields.io/pypi/l/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)

# bs2json

Convert BeautifulSoup4 HTML elements to JSON.

## Installation

```bash
pip install -U bs2json
```

## Quick Start

```python
from bs2json import BS2Json

html = """
<html>
<head><title>My Page</title></head>
<body>
    <h1>Welcome</h1>
    <p class="intro">Hello <b>world</b></p>
</body>
</html>
"""

converter = BS2Json(html)
result = converter.convert()
# {'html': {'head': {'title': 'My Page'}, 'body': {'h1': 'Welcome', 'p': {'attrs': {'class': ['intro']}, 'text': 'Hello', 'b': 'world'}}}}
```

## Features

### Convert Specific Tags

```python
converter = BS2Json(html)

# By tag name
converter.convert('body')

# By CSS class
converter.convert(class_='intro')
```

### Convert Multiple Tags

```python
converter = BS2Json(html)

# As a list of individual results
converter.convert_all('a')

# Grouped by tag name
converter.convert_all('a', join=True)
```

### Preserve Element Order

By default, sibling elements are grouped by tag name. Use `keep_order=True` to preserve the original document order:

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
html = '<html><body><!-- note --><p>  hello  </p></body></html>'

# Exclude HTML comments (included by default)
BS2Json(html, include_comments=False).convert()

# Preserve leading/trailing whitespace (stripped by default)
BS2Json(html, strip=False).convert()
```

### Custom Labels

Change the JSON key names used for attributes, text, and comments:

```python
converter = BS2Json(html)
converter.labels(attrs='attributes', text='content', comment='notes')
converter.convert()
```

### Save and Prettify

```python
converter = BS2Json(html)
converter.convert()

# Save to file
converter.save('output.json')

# Pretty-print
converter.prettify()
```

### Extension Mode

Add `.to_json()` directly to every BeautifulSoup Tag:

```python
from bs4 import BeautifulSoup
from bs2json import install, remove

install()

soup = BeautifulSoup(html, 'html.parser')
soup.find('body').to_json()
soup.body.to_json(keep_order=True)

remove()  # clean up when done
```

### Configuration Object

All options are stored in a `ConversionConfig` dataclass:

```python
from bs2json import BS2Json, ConversionConfig

converter = BS2Json(html, keep_order=True, strip=False)
print(converter.config)
# ConversionConfig(attr_name='attrs', text_name='text', comment_name='comment',
#                  include_comments=True, strip=False, keep_order=True)
```

## API Reference

| Method | Description |
|--------|-------------|
| `BS2Json(html, *, include_comments=True, strip=True, keep_order=False)` | Initialize from HTML string, Tag, or BeautifulSoup |
| `.convert(element=None, **kwargs)` | Convert a single tag to JSON |
| `.convert_all(elements=None, join=False, **kwargs)` | Convert multiple tags to a list |
| `.labels(attrs=..., text=..., comment=...)` | Change JSON key names |
| `.save(path, prettify=True, indent=4)` | Save last result to file |
| `.prettify()` | Pretty-print last result |
| `.config` | Access the `ConversionConfig` dataclass |

## Contributing

We appreciate all contributions. If you are planning to contribute bug-fixes, please do so without further discussion.

If you plan to contribute new features, please first open an issue and discuss the feature with us.

<a href="https://github.com/MrDebugger/bs2json/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MrDebugger/bs2json"/>
</a>
