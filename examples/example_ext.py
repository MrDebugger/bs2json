"""Extension mode: adds .to_json() directly to every bs4 Tag."""

from bs4 import BeautifulSoup
from bs2json import install, remove

# Install the extension
install()

html = '<html><head><title>Page Title</title></head><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>'
soup = BeautifulSoup(html, 'html.parser')

# Convert the return of find() to JSON
print("body:", soup.find('body').to_json())

# Convert the soup object to JSON
print("soup:", soup.to_json())

# Convert any tag to JSON
print("body tag:", soup.body.to_json())

# With options
print("group_by_tag:", soup.body.to_json(group_by_tag=True))

# Clean up when done
remove()
print("Extension removed:", not hasattr(soup.body, 'to_json'))
