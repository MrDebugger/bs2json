# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-17

### Breaking Changes

- **Ordered output is now the default.** Elements preserve their original document order instead of being grouped by tag name. Multiple children are wrapped in `{"children": [...]}`.
- **`keep_order` parameter replaced by `group_by_tag`** (default `False`). Set `group_by_tag=True` to restore the old grouped behavior.
- **Removed deprecated aliases:** `bs2json` (lowercase), `convertAll()`, `toJson()` — use `BS2Json`, `convert_all()`, `to_json()`.
- **Package restructured** into focused modules: `models.py`, `serializer.py`, `converter.py`, `extension.py`. The monolithic `bs2json.py` has been removed.
- **Migrated from `setup.py` to `pyproject.toml`.**
- **Dependency changed** from `bs4` shim to `beautifulsoup4` (the canonical package).

### Added

- `ConversionConfig` dataclass — structured configuration object accessible via `converter.config`.
- `group_by_tag` option — opt-in for the legacy grouped-by-tag-name output format.
- `__repr__` on `BS2Json` for debugging friendliness.
- 27 tests (up from 6).

### Fixed

- **Class-level mutable state bug** — `__labels`, `last_obj`, and `soup` were shared across all instances, causing cross-instance corruption.
- **`convert_all()` crash** when called with no arguments while soup was set.
- **`include_comments=False`** now properly excludes HTML comments (previously fell through to `NavigableString`).
- **`NoReturn` type hints** replaced with correct `None` return type.
- **Ordered output with attributes** — elements with attrs now consistently produce `{"attrs": {...}, "children": [...]}` instead of appending attrs as a list item.

## [0.1.2] - 2023-03-01

### Added

- Ability to initialize from a string (auto-parses with BeautifulSoup).
- `convert()` accepts string element names and `find()` kwargs.
- `convert_all()` with `join` parameter.
- `include_comments` option.
- `strip` option for whitespace control.
- `labels()` for custom JSON key names.
- `save()` to write results to file.
- `prettify()` for pretty-printing.
- Extension mode via `install()`/`remove()`.
- Context manager support.

## [0.0.2] - 2022-01-01

### Fixed

- Returning null for tags like `<img>` with no children.
- `convertAll` default list issue.

## [0.0.1] - 2021-01-01

### Added

- Initial release.
- Basic HTML-to-JSON conversion via `BS2Json`.
