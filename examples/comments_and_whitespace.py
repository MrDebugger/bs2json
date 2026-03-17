"""Controlling comment inclusion and whitespace stripping."""

from bs2json import BS2Json

html = '<html><body><!-- TODO: fix layout --><p>  hello world  </p><!-- end --></body></html>'

# Default: comments included, whitespace stripped
print("Default:")
print(BS2Json(html).convert())

# Exclude comments
print("\nNo comments:")
print(BS2Json(html, include_comments=False).convert())

# Preserve whitespace
print("\nPreserve whitespace:")
print(BS2Json(html, strip=False).convert())

# Both: no comments + preserve whitespace
print("\nNo comments + preserve whitespace:")
print(BS2Json(html, include_comments=False, strip=False).convert())
