"""Converting multiple tags at once."""

from bs2json import BS2Json

html = """
<html><body>
    <a href="/one" class="nav">Home</a>
    <a href="/two" class="nav">About</a>
    <a href="/three" class="nav">Contact</a>
</body></html>
"""

converter = BS2Json(html)

# Individual results
print("As list:")
for item in converter.convert_all('a'):
    print(" ", item)

# Grouped by tag name
print("\nJoined:")
result = converter.convert_all('a', join=True)
print(result)

# Using find_all kwargs
print("\nBy class:")
result = converter.convert_all(class_='nav')
print(result)

# No args = all tags
print("\nAll tags:")
result = converter.convert_all()
print(f"Found {len(result)} tags")
