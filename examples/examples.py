"""Basic usage examples for bs2json."""

from bs2json import BS2Json, ConversionConfig

html = """
<html>
<head><title>My Page</title></head>
<body>
    <h1>Welcome</h1>
    <p class="intro">This is a <b>sample</b> page.</p>
    <ul>
        <li><a href="/one">Link 1</a></li>
        <li><a href="/two">Link 2</a></li>
    </ul>
    <p class="footer">Footer text</p>
</body>
</html>
"""

# --- Basic conversion ---
converter = BS2Json(html)
result = converter.convert()
print("Full document:")
converter.prettify()
print()

# --- Convert a specific tag ---
converter = BS2Json(html)
result = converter.convert('body')
print("Body only:", result)
print()

# --- Find and convert by CSS class ---
converter = BS2Json(html)
result = converter.convert(class_='intro')
print("Intro paragraph:", result)
print()

# --- Convert all matching tags ---
converter = BS2Json(html)
links = converter.convert_all('a')
print("All links:", links)
print()

# --- Join same tags into one ---
converter = BS2Json(html)
links = converter.convert_all('a', join=True)
print("Joined links:", links)
print()

# --- Custom labels ---
converter = BS2Json(html)
converter.labels(attrs='attributes', text='content')
result = converter.convert('body')
print("Custom labels:", result)
print()

# --- Preserve element order (keep_order) ---
ordered = BS2Json(html, keep_order=True)
result = ordered.convert()
print("Ordered output:")
ordered.prettify()
print()

# --- HTML comments ---
comment_html = '<html><body><!-- TODO: fix this --><p>visible</p><!-- another comment --></body></html>'
print("include_comments=True:", BS2Json(comment_html, include_comments=True).convert())
print("include_comments=False:", BS2Json(comment_html, include_comments=False).convert())
print()

# --- Strip whitespace control ---
ws_html = '<html><body><p>  hello world  </p></body></html>'
print("strip=True:", BS2Json(ws_html, strip=True).convert())
print("strip=False:", BS2Json(ws_html, strip=False).convert())
print()

# --- Save to file ---
converter = BS2Json(html)
converter.convert()
converter.save('bs2json-output.json')
print("Saved to bs2json-output.json")
print()

# --- Context manager ---
with BS2Json(html) as converter:
    result = converter()  # __call__ is a shortcut for convert()
    print("Context manager:", result.keys())
print()

# --- Access config directly ---
converter = BS2Json(html, keep_order=True, strip=False)
print("Config:", converter.config)
