"""Basic HTML to JSON conversion."""

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

# Full document
converter = BS2Json(html)
result = converter.convert()
converter.prettify()

# Specific tag by name
print("\nBody only:")
print(BS2Json(html).convert('body'))

# By CSS class
print("\nBy class:")
print(BS2Json(html).convert(class_='intro'))

# By attribute
print("\nBy href:")
print(BS2Json(html).convert('a', href='/link1'))
