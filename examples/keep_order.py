"""Preserving element order instead of grouping by tag name."""

from bs2json import BS2Json

html = """
<html><body>
    <h2>Chapter 1</h2>
    <p>First paragraph.</p>
    <h2>Chapter 2</h2>
    <p>Second paragraph.</p>
    <h2>Chapter 3</h2>
    <p>Third paragraph.</p>
</body></html>
"""

# Default: groups by tag name (loses order)
print("Grouped (default):")
result = BS2Json(html).convert()
body = result['html']['body']
print(f"  h2: {body['h2']}")
print(f"  p:  {body['p']}")

# Ordered: preserves document sequence
print("\nOrdered (keep_order=True):")
result = BS2Json(html, keep_order=True).convert()
html_content = result['html']
for item in html_content:
    if isinstance(item, dict) and 'body' in item:
        for child in item['body']:
            tag = list(child.keys())[0]
            print(f"  <{tag}> {child[tag]}")
