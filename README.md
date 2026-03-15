# ISeekGod: Token Ascension Metrics

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║  ✨ ISeekGod - Token Ascension Engine                    ║
║                                                            ║
║  Analyze token growth through divine metrics             ║
║  Ascension Index • Community Health • Karma Rating        ║
║  Soul Purity • Divine Alignment                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

## Overview

ISeekGod measures token quality through 5 core metrics, delivered in 4 languages:
- **Python** — Core analysis engine
- **Go** — Fast CLI tool
- **Rust** — High-performance SDK
- **TypeScript** — Web dashboard interface

## Key Metrics (0-100)

| Metric | Meaning |
|--------|---------|
| **Ascension Index** | Growth trajectory + consistency |
| **Community Health** | Holder growth + trading volume |
| **Karma Rating** | Volatility resistance (sustainability) |
| **Soul Purity** | Pump-dump attack resistance |
| **Divine Alignment** | 6-level token classification (ENLIGHTENED → LOST) |

## Installation

```bash
# Python
pip install -r requirements.txt
pytest tests/  # 40+ tests

# Go
cd go && go run main.go analyze TOKEN

# Rust
cd sdk && cargo test --release

# TypeScript
cd ts && npm install && npm run build
```

## Usage

### Python

```python
from ascension import AscensionEngine, TokenSnapshot
from datetime import datetime

engine = AscensionEngine()

# Add snapshots and analyze
snapshot = TokenSnapshot(
    timestamp=datetime.utcnow(),
    market_cap=10000.0,
    holder_count=100,
    trading_volume=1000.0,
    price=0.001,
)
engine.add_snapshot("TOKEN", snapshot)
metrics = engine.analyze_token("TOKEN")
print(f"Ascension: {metrics.ascension_index}, Alignment: {metrics.divine_alignment}")
```

### Go

```bash
cd go
go run main.go analyze DIVINE
```

### Rust

```bash
cd sdk && cargo test --release
```

## Architecture

50+ tests across Python implementations. Real logic in Go (not hardcoded). 11 inline Rust tests. Multi-language sync ensures consistency.

See CLAUDE.md for technical details.
