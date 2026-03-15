# ISeekGod — Project Context

## What is this

Multi-language token ascension metrics engine. Analyzes token growth through 5 core metrics, assigning 6-level divine alignment classification.

Designed for traders and analysts evaluating token quality based on real data, not hype.

## Purpose

Standard crypto metrics (market cap, holder count, price) can be gamed. ISeekGod measures:
- **Real growth** (ascension index) — not just hype cycles
- **Sustainability** (community health + karma rating) — organic adoption
- **Resistance** (soul purity) — pump-dump attack immunity
- **Overall credibility** (divine alignment) — 6-level classification

## Stack

- **Python 3.10+** — Core analysis engine, 40+ tests
- **Go 1.22** — Fast CLI tool with real analysis logic
- **Rust 2021** — High-performance SDK with 11 inline tests
- **TypeScript 5.4** — Web dashboard interface

## Architecture

```
Transaction Data
    ↓
AscensionEngine (Python)
  • TokenSnapshot input
  • 5 metric calculations
  • Divine alignment assignment
    ↓
    ├→ Python API (direct use)
    ├→ Go CLI (batch processing)
    ├→ Rust SDK (performance)
    └→ TypeScript (web interface)
```

## Core Metrics (0-100)

### 1. Ascension Index
```
ascension = (growth_score × 0.6) + (consistency × 0.4)

growth_score = min(total_growth / 3, 100)
  where total_growth = (latest_mc / first_mc - 1) × 100, capped at 300%

consistency = max(0, 100 - std_dev × 50)
  where std_dev = market_cap volatility coefficient
```
Measures sustainable growth, not volatile spikes.

### 2. Community Health
```
health = (holder_growth × 0.7) + (volume_score × 0.3)

holder_growth = min((latest - first) / first × 100 / 2, 100)
volume_score = 1.0 if avg_volume > 100k else 0.5
```
Reflects real adoption, not bot activity.

### 3. Karma Rating
```
karma = max(0, 100 - avg_volatility)

where avg_volatility = average daily % change in market cap
```
Lower volatility = higher karma = sustainable.

### 4. Soul Purity
```
purity = max(0, 100 - spike_ratio × 100)

where spike = price up >30%, then down >20%
```
Detects pump-and-dump attack patterns.

### 5. Safety Score
```
safety = (ascension + health + karma) / 3
```
Quick overall assessment.

## Divine Alignment

6-level classification based on ascension_index:

| Level | Index | Meaning |
|-------|-------|---------|
| ENLIGHTENED | 90-100 | Sustained excellence |
| ASCENDING | 75-89 | Consistent profitability |
| GROWING | 60-74 | Good patterns |
| STABLE | 40-59 | Mixed signals |
| DESCENDING | 20-39 | Losing momentum |
| LOST | 0-19 | Noise |

## Key Files

| Path | Language | Role |
|------|----------|------|
| ascension.py | Python | AscensionEngine, TokenSnapshot, 5 metrics |
| tests/ | Python | 40+ tests: core, metrics, alignment |
| go/ | Go | CLI analyzer, types, real calculation logic |
| sdk/ | Rust | RizzOracle SDK with 11 inline tests |
| ts/ | TypeScript | AscensionEngine interface, type safety |

## Testing

**40+ Python tests:**
- test_ascension.py (11 tests) — Core functionality
- test_metrics.py (11 tests) — Individual metric calculations
- test_alignment.py (8+ tests) — Divine alignment boundaries

**11 Rust inline tests** — Full SDK coverage

**100% pass rate maintained**

## Development Workflow

```bash
# Branch strategy
git checkout -b feature/your-feature
# Make changes
pytest tests/ -v
git add .
git commit -m "feat(module): description"
git push origin feature/your-feature

# Then create PR to main
```

## Commit Style

```
feat(module): description
fix(module): fix description
test(module): add test description
docs: update docs
chore: maintenance task
```

**Always include:**
```
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

## Performance

- Python: <100ms for 100 snapshots
- Go CLI: Real analysis, not hardcoded (generates mock data for demo)
- Rust: Ready for high-frequency indexing
- TypeScript: Real-time web dashboard

## Things to Remember

- Core calculations are identical across all languages (Python is reference)
- Snapshots must be sorted by timestamp before analysis
- Days elapsed defaults to 1 to avoid division by zero
- Market cap growth capped at 300% for ascension calculation
- Soul purity requires 3+ snapshots (otherwise 50.0)
- All metrics normalized to 0-100 for comparison
- Divine alignment determined purely by ascension_index threshold
