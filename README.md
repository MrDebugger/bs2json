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
from bs4 import BeautifulSoup
from requests import get
from bs2json import bs2json

html = get('https://ijazurrahim.com').text

soup = BeautifulSoup(html,'lxml')
converter = bs2json()

tags = soup.findAll('a')
json = converter.convertAll(tags,join=True)
print(json)
```

Output
----

Upon running the Above Program, you will get the following output

```python3
[{'a': {'i': {'attributes': {'class': ['fa', 'fa-facebook']}}, 'attributes': {'href': 'https://web.facebook.com/MisterDebugger'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-instagram']}}, 'attributes': {'href': 'https://www.instagram.com/MisterDebugger'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-twitter']}}, 'attributes': {'href': 'https://www.twitter.com/muibraheem96'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-stack-overflow']}}, 'attributes': {'href': 'https://www.stackoverflow.com/users/9140224/ijaz-ur-rahim'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-linkedin']}}, 'attributes': {'href': 'https://www.linkedin.com/in/muibraheem96'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-github']}}, 'attributes': {'href': 'https://www.github.com/MrDebugger'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-building']}}, 'attributes': {'href': 'https://www.upwork.com/freelancers/~01c44a17a8ed828883'}}}, {'a': {'i': {'attributes': {'class': ['fa', 'fa-youtube']}}, 'attributes': {'href': 'https://www.youtube.com/ijazurrahim'}}}]
```

Other Methods
----

- There are total 3 methods `labels()`, `convert()` and `convertAll()` where `convert()` and `convertAll()` takes two parameters of type `bs4.element.Tag`, `dict` (optional) and three parameters of type `bs4.ResultSet`, `list` (optional), `bool` (default: False) respectively. 
- `labels()` method takes two positional arguments `attributes` and `text` which replaces the respective names in output json.
- `convert()` method takes `element` (bs4.element.Tag) and `json` (dict: optional) as arguments. Whereas `element` is result of `BeautifulSoup().find()` and `json` is an empty dictionary or already constructed dictionary.
- `convertAll()` method takes `elements` (bs4.element.Tag), `List` (list: optional) and `join` (bool: default=False) as arguments. Whereas `elements` is result of `BeautifulSoup().findAll()`, `list` is an empty list or already constructed list and `join` is a boolean value. When `join` becomes `True`, same tags will append to one list and assinged to one tag name resulting a dictionary. For more information, see example files.


Contributing
----

We appreciate all contributions. If you are planning to contribute any bug-fixes, please do so without further discussions.

If you plan to contribute new features etc. please first open an issue or reuse an exisiting issue, and discuss the feature with us. We will discuss with you on the issue timely or set up conference calls if needed.

We appreciate all contributions and thank all the contributors!

<a href = "https://github.com/MrDebugger/bs2json/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=MrDebugger/bs2json"/>
</a>
