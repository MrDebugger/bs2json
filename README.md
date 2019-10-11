[![PyPi version](https://img.shields.io/pypi/v/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPi pyversions](https://img.shields.io/pypi/pyversions/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)
[![PyPi license](https://img.shields.io/pypi/l/bs2json.svg)](https://pypi.python.org/pypi/bs2json/)

Convert HTML Tags of BeautifulSoup class to JSON data using.

Installation
----

This package is available on PyPi. Just use `pip install -U bs2json` to install it. Then you can import it using `from bs2json import bs2json`.

Example Syntax
----

```python3
from bs4 import BeautifulSoup
from requests import get
from bs2json import bs2json

html = get('https://ijazurrahim.com').text

soup = BeautifulSoup(html,'lxml')
converter = bs2json()

tag = soup.find('ul')
json = converter.convert(tag)
print(json)
```

Output
----

Upon running the Above Program, you will get the following output

```python3
{'ul': {'attributes': {'class': ['nav', 'nav-justified', 'justify-content-center']}, 'li': [{'attributes': {'class': ['nav-item'], 'onclick': "window.location='#home';change();"}, 'a': {'attributes': {'href': '#home'}, 'text': 'Home'}, 'text': ''}, {'attributes': {'class': ['nav-item'], 'onclick': "window.location='#skills';change();"}, 'a': {'attributes': {'href': '#skills'}, 'text': 'Skills'}, 'text': ''}, {'attributes': {'class': ['nav-item'], 'onclick': "window.location='#contact';change();"}, 'a': {'attributes': {'href': '#contact'}, 'text': 'Contact'}, 'text': ''}, {'attributes': {'class': ['nav-item'], 'onclick': "window.location='#blog';change();"}, 'a': {'attributes': {'href': '#blog'}, 'text': 'Blog'}, 'text': ''}], 'text': ''}}
```

Other Methods
----

- There are total 2 methods `convert()` and `convertAll()` which takes two parameters of type `bs4.element.Tag`, `dict` and `bs4.ResultSet`, `list` respectively. 
- `convert()` method takes `bs4.element.Tag` and `dict` as arguments. `bs4.element.Tag` is result of `soup.find()` and `dict` is an empty dictionary or already constructed dictionary.
- `convertAll()` also method takes `bs4.ResultSet` and `list` as arguments. `bs4.ResultSet` is result of `soup.findAll()` and `list` is an empty list or already constructed list.

