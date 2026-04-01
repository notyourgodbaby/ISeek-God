# Contributing to ISeekGod

We welcome contributions from developers of all levels. Here's how to get started.

## Setup

```bash
# Clone and install
git clone https://github.com/notyourgodbaby/ISeekGod.git
cd iseekgod

# Python setup
pip install -r requirements.txt
pytest tests/

# Go setup
cd go && go run main.go help

# Rust setup
cd sdk && cargo test --release

# TypeScript setup
cd ts && npm install && npm run build
```

## Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `pytest tests/ -v`
4. Commit with proper message format (see below)
5. Push and open a PR

## Commit Message Format

```
feat(module): add new feature
fix(module): fix bug
test(module): add test
docs: update documentation
chore: maintenance

Include:
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

## Code Style

- Python: PEP 8
- Go: Use `gofmt`
- Rust: Use `rustfmt`
- TypeScript: Use strict types

## Testing

All submissions must pass tests:

```bash
# Python (40+ tests)
pytest tests/ -v

# Rust (11 inline tests)
cd sdk && cargo test --release

# Go (compile check)
cd go && go build -v ./...

# TypeScript (build check)
cd ts && npm run build
```

## Pull Request

- Describe what and why
- Reference any issues
- Ensure tests pass
- Follow commit style

Thank you for contributing!
