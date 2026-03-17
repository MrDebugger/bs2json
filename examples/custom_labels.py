"""Customizing JSON key names for attributes, text, and comments."""

from bs2json import BS2Json

html = '<html><body><!-- note --><p class="main">Hello <b>world</b></p></body></html>'

# Default labels
print("Default labels:")
result = BS2Json(html).convert()
print(result)

# Custom labels
print("\nCustom labels:")
converter = BS2Json(html)
converter.labels(attrs='attributes', text='content', comment='notes')
result = converter.convert()
print(result)

# Labels via constructor kwargs
print("\nVia constructor:")
converter = BS2Json(html, attr_name='@', text_name='#text', comment_name='#comment')
result = converter.convert()
print(result)
