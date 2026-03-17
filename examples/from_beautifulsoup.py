"""Using bs2json with existing BeautifulSoup objects."""

from bs4 import BeautifulSoup
from bs2json import BS2Json

html = """
<html><body>
    <div id="content">
        <h1>Title</h1>
        <p>Paragraph 1</p>
        <p>Paragraph 2</p>
    </div>
    <footer>Footer text</footer>
</body></html>
"""

# Parse with BeautifulSoup first
soup = BeautifulSoup(html, 'html.parser')

# Pass the soup object directly
print("From soup:")
print(BS2Json(soup).convert())

# Pass a specific tag
div = soup.find('div', id='content')
print("\nFrom tag:")
print(BS2Json(div).convert())

# Convert on-the-fly without pre-setting soup
print("\nOn-the-fly:")
converter = BS2Json()
print(converter.convert(soup.footer))
