# ISeekGod - Project Context

## Overview

Token ascension metrics engine for analyzing Solana token growth. Multi-language implementation.

## Architecture

### Core Metrics (0-100)
1. **Ascension Index** — Growth trajectory + consistency
2. **Community Health** — Holder growth + volume
3. **Karma Rating** — Volatility resistance  
4. **Soul Purity** — Pump-dump resistance
5. **Safety Score** — Average of above 3

### Divine Alignment (6 levels)
- ENLIGHTENED (90-100)
- ASCENDING (75-89)
- GROWING (60-74)
- STABLE (40-59)
- DESCENDING (20-39)
- LOST (0-19)

## Stack

- Python 3.10+ — Core engine
- Go 1.22 — CLI tool
- Rust 2021 — SDK
- TypeScript 5.4 — Interface

## Key Files

| File | Purpose |
|------|---------|
| ascension.py | Core AscensionEngine class |
| go/main.go | CLI implementation |
| sdk/src/lib.rs | Rust SDK |
| ts/src/index.ts | TypeScript interface |

## Installation

```bash
pip install -r requirements.txt
pytest tests/
```

## Commit Style

```
feat: add feature
fix: fix bug
docs: update docs
test: add tests
chore: maintenance
```

Include: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`

## Testing

All tests must pass. Target 50+ tests across Python implementations.
