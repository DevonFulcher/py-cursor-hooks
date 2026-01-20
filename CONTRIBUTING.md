# Contributing

## Development Setup

```bash
# Clone the repository
git clone https://github.com/devonfulcher/py-cursor-hooks.git
cd py-cursor-hooks

# Install dependencies (including dev tools)
task install

# Install pre-commit hooks
task pre-commit:install
```

## Running Tests

```bash
task test
```

## Linting and Formatting

```bash
# Run all checks
task check

# Auto-fix issues
task fix
```

## Release Process

1. **Update the version** in `pyproject.toml`:

   ```toml
   [project]
   version = "X.Y.Z"
   ```

2. **Commit the version bump**:

   ```bash
   git add pyproject.toml
   git commit -m "Bump version to X.Y.Z"
   git push
   ```

3. **Create a GitHub release**:
   - Go to the repository's Releases page
   - Click "Draft a new release"
   - Create a new tag (e.g., `vX.Y.Z`)
   - Add release notes
   - Click "Publish release"

4. The GitHub Action will automatically build and publish to PyPI.
