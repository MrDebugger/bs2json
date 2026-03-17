"""Working with ConversionConfig directly."""

from bs2json import BS2Json, ConversionConfig

html = '<html><body><p class="x">hello</p></body></html>'

# Config is created automatically from constructor args
converter = BS2Json(html, keep_order=True, strip=False)
print("Auto config:", converter.config)

# Modify config after creation
converter.config.keep_order = False
converter.config.strip = True
print("Modified:   ", converter.config)

# Config changes affect subsequent conversions
result = converter.convert()
print("Result:", result)

# Inspect individual fields
cfg = converter.config
print(f"\nattr_name: {cfg.attr_name}")
print(f"text_name: {cfg.text_name}")
print(f"comment_name: {cfg.comment_name}")
print(f"include_comments: {cfg.include_comments}")
print(f"strip: {cfg.strip}")
print(f"keep_order: {cfg.keep_order}")
