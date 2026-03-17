"""Grouped-by-tag output as an opt-in via group_by_tag=True."""

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

# Default: preserves document order
print("Ordered (default):")
result = BS2Json(html).convert()
for child in result['html']['body']['children']:
    tag = list(child.keys())[0]
    print(f"  <{tag}> {child[tag]}")

# Grouped: groups all elements by tag name (loses document order)
print("\nGrouped (group_by_tag=True):")
result = BS2Json(html, group_by_tag=True).convert()
body = result['html']['body']
print(f"  h2: {body['h2']}")
print(f"  p:  {body['p']}")
