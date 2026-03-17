# Contributing to bs2json

We appreciate all contributions! Here's how to get involved.

## Bug Fixes

If you're fixing a bug, please go ahead and submit a pull request without prior discussion.

Include:
- A test that reproduces the bug (fails before your fix, passes after)
- A clear commit message explaining what was broken and why

## New Features

If you plan to contribute new features, **please first open an issue** and discuss the feature with us before writing code. This avoids wasted effort on features that may not fit the project's direction.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/MrDebugger/bs2json.git
cd bs2json

# Install in editable mode
pip install -e .

# Run tests
python3 -m pytest tests/tests.py -v
```

## Project Structure

```
bs2json/
├── __init__.py       # Public API exports
├── models.py         # ConversionConfig dataclass
├── serializer.py     # Stateless recursive conversion engine
├── converter.py      # BS2Json orchestrator class
└── extension.py      # install()/remove() monkey-patching
```

## Testing

All changes must include tests. Run the full suite before submitting:

```bash
python3 -m pytest tests/tests.py -v
```

- Tests live in `tests/tests.py`
- Expected outputs for the standard test HTML are in `tests/expected_output.py`
- Aim for tests that verify **behavior**, not implementation details

## Code Style

- Follow existing patterns in the codebase
- Use type hints for public method signatures
- Keep files focused — one responsibility per module
- No new dependencies unless absolutely necessary

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): Breaking changes to the public API (removed/renamed methods, changed output format, removed parameters)
- **MINOR** (0.x.0): New features that are backward-compatible (new parameters with defaults, new methods, new exports)
- **PATCH** (0.0.x): Bug fixes and internal improvements that don't change the public API

### What counts as the public API

- `BS2Json` class and all its public methods
- `ConversionConfig` dataclass and its fields
- `install()` and `remove()` functions
- The JSON output structure for both default and `group_by_tag` modes

### Examples

| Change | Version bump |
|--------|-------------|
| Fix a bug in `convert()` | PATCH |
| Add a new option like `strip=True` | MINOR |
| Change default output format | MAJOR |
| Rename `convert_all()` to something else | MAJOR |
| Add a new method to `BS2Json` | MINOR |
| Restructure internal modules (no API change) | PATCH |

## Pull Request Process

1. Create a feature branch from `master`
2. Make your changes with tests
3. Run the full test suite
4. Submit a PR with a clear description of what and why

## Contributors

<a href="https://github.com/MrDebugger/bs2json/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MrDebugger/bs2json"/>
</a>
