# bs2json Package Restructure Design

## Goal

Split the monolithic `bs2json.py` (~355 lines) into focused modules with a dataclass-based config model. Clean break — no backward compatibility shims.

## Current Structure

```
bs2json/
├── __init__.py    # Exports, deprecated aliases, extension monkey-patching
└── bs2json.py     # Everything: config, parsing, serialization, output
```

Problems:
- Single file does 4 jobs (config, conversion orchestration, recursive serialization, output)
- Config is a private `__labels` dict + loose boolean attributes
- Extension logic mixed with exports and deprecated aliases
- Name-mangled `__labels` makes the serializer tightly coupled to the class

## Target Structure

```
bs2json/
├── __init__.py       # Public API exports only
├── models.py         # ConversionConfig dataclass
├── serializer.py     # Stateless recursive serialization engine
├── converter.py      # BS2Json orchestrator class
└── extension.py      # install()/remove() monkey-patching
```

## Module Specifications

### `models.py`

Single dataclass replacing the `__labels` dict and loose boolean flags:

```python
from dataclasses import dataclass

@dataclass
class ConversionConfig:
    attr_name: str = "attrs"
    text_name: str = "text"
    comment_name: str = "comment"
    include_comments: bool = True
    strip: bool = True
    keep_order: bool = False
```

This is the single source of truth for conversion options. Passed by reference so mutations via `labels()` propagate.

### `serializer.py`

Stateless recursive conversion engine. Takes a `ConversionConfig` and bs4 elements, returns dicts/lists/strings.

```python
class Serializer:
    def __init__(self, config: ConversionConfig):
        self.config = config

    def to_json(self, element) -> Union[Dict, List, str]:
        """Recursive entry point. Converts bs4 element to JSON-compatible structure."""

    def _tag(self, element) -> Union[Dict, List, str]:
        """Process a single Tag element with its attributes and children."""

    def _fix(self, json: dict) -> None:
        """Post-process grouped children: unwrap single-element lists, extract text."""

    def _get_name(self, element) -> str:
        """Return the label name for a bs4 element (tag name, text label, or comment label)."""
```

Key properties:
- **Stateless**: no `last_obj`, no `soup`. Just config + element in, dict out.
- **No name mangling**: config fields accessed via `self.config.attr_name` etc. — clean, readable.
- Methods that were `__private` become `_internal` (single underscore) since they're in their own module now.

### `converter.py`

User-facing orchestrator. Owns soup, config, last_obj. Delegates serialization.

```python
class BS2Json:
    def __init__(self, soup=None, features='html.parser', *,
                 include_comments=True, strip=True, keep_order=False, **kwargs):
        # Build ConversionConfig from kwargs
        # Parse soup if string
        # Create Serializer

    def __enter__(self): ...
    def __exit__(self, ...): ...
    def __repr__(self): ...
    def __call__(self, *args, **kwargs): ...

    def labels(self, **kwargs) -> None:
        """Mutate config labels (attrs, text, comment)."""

    def convert(self, element=None, json=None, *, inplace=False, **kwargs) -> Dict:
        """Convert a single tag to JSON. Delegates to self._serializer.to_json()."""

    def convert_all(self, elements=None, lst=None, *, join=False, **kwargs) -> List:
        """Convert multiple tags to JSON list."""

    def save(self, file_obj='bs2json-output.json', /, mode='w', encoding='utf-8', *, prettify=True, indent=4, **kwargs):
        """Save last_obj to file."""

    def prettify(self):
        """Pretty-print last_obj."""
```

Key properties:
- Public API signature is **identical** to current — all 23 tests pass unchanged.
- Internally creates a `Serializer` instance and delegates `to_json` calls to it.
- `labels()` mutates `self.config` which the serializer reads by reference.

### `extension.py`

Monkey-patching logic, extracted from `__init__.py`:

```python
from bs4 import element, BeautifulSoup
from .models import ConversionConfig
from .converter import BS2Json

def to_json(tag, include_comments=True, strip=True, keep_order=False,
            attr_name="attrs", text_name="text", comment_name="comment"):
    """Extension method added to element.Tag via install()."""
    ...

def install():
    if not hasattr(element.Tag, 'to_json'):
        element.Tag.to_json = to_json

def remove():
    if hasattr(element.Tag, 'to_json'):
        del element.Tag.to_json
```

### `__init__.py`

Clean exports only:

```python
from .converter import BS2Json
from .models import ConversionConfig
from .extension import install, remove

__all__ = ["BS2Json", "ConversionConfig", "install", "remove"]
```

No deprecated aliases. No logic.

## What Changes for Users

**Removed (clean break):**
- `from bs2json import bs2json` (lowercase alias) — use `BS2Json`
- `bs2json.convertAll()` — use `convert_all()`
- `bs2json.toJson()` — use `to_json()`

**Added:**
- `from bs2json import ConversionConfig` — direct config construction
- Config object accessible via `converter.config`

**Unchanged:**
- `BS2Json(html)`, `.convert()`, `.convert_all()`, `.save()`, `.prettify()`, `.labels()`
- `install()`, `remove()`
- All constructor parameters
- All output formats

## Testing

All 23 existing tests must pass with zero changes (except removing any tests that specifically test the removed deprecated aliases — there are none currently).

## Constraints

- No new dependencies
- Python 3.8+ (dataclasses are stdlib since 3.7)
- Delete `bs2json.py` after migration (replaced by `converter.py` + `serializer.py` + `models.py`)
