"""Saving conversion results to files."""

import io
import json
from bs2json import BS2Json

html = '<html><body><h1>Title</h1><p>Content</p></body></html>'

converter = BS2Json(html)
converter.convert()

# Save to file (pretty-printed, 4-space indent)
converter.save('output.json')
print("Saved to output.json")

# Save compact (no indentation)
converter.save('compact.json', prettify=False)
print("Saved to compact.json")

# Save with custom indent
converter.save('indent2.json', indent=2)
print("Saved to indent2.json")

# Save to a file-like object
buf = io.StringIO()
converter.save(buf)
buf.seek(0)
print("\nFrom buffer:")
print(json.loads(buf.read()))

# Pretty-print to stdout
print("\nPretty-print:")
converter.prettify()

# Clean up
import os
for f in ['output.json', 'compact.json', 'indent2.json']:
    os.unlink(f)
