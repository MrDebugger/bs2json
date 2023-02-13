[![PyPi version](https://img.shields.io/pypi/v/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPi pyversions](https://img.shields.io/pypi/pyversions/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPi license](https://img.shields.io/pypi/l/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)

Convert HTML Tags of BeautifulSoup class to JSON data.

Installation
----

This package is available on PyPi. Just use `pip install -U bs2json` to install it. Then you can import it using `from bs2json import bs2json`.

Example Syntax
----

```python3
from bs2json import BS2Json

html = '<html><head><title>Page Title</title></head><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>'
bs2json = BS2Json(html)

# Convert soup to JSON
json_obj = bs2json.convert()

# Save JSON to file
bs2json.save()

# Print prettified output
bs2json.prettify()

```

Plus point
---

You can also use the module methods as an extension to the `element.Tag`.
For more information, see the `example_ext.py` file from examples


What's new
---

- Ability to initialize the bs4 object from given string
- Converts a single bs4 tag or a tag matching the given string to a JSON object
- Option to include or exclude comments in the JSON representation
- Option to remove whitespaces from the start and end of text
- Ability to save the converted object to a file
- Ability to prettify the output of the last converted object
- Option to set custom labels for converting BeautifulSoup elements to JSON


Contributing
----

We appreciate all contributions. If you are planning to contribute any bug-fixes, please do so without further discussions.

If you plan to contribute new features etc. please first open an issue or reuse an exisiting issue, and discuss the feature with us. We will discuss with you on the issue timely or set up conference calls if needed.

We appreciate all contributions and thank all the contributors!

<a href = "https://github.com/MrDebugger/bs2json/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=MrDebugger/bs2json"/>
</a>
