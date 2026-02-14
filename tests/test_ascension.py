"""Tests for AscensionEngine core functionality."""
import pytest
from datetime import datetime, timedelta
from ascension import AscensionEngine, TokenSnapshot, DivineAlignment


@pytest.fixture
def engine():
    return AscensionEngine()


class TestAscensionEngine:
    def test_empty_engine(self, engine):
        result = engine.analyze_token("nonexistent")
        assert result is None

    def test_single_snapshot(self, engine):
        snapshot = TokenSnapshot(
            timestamp=datetime.utcnow(),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.token_name == "TEST"
        assert metrics.current_market_cap == 10000.0

    def test_multiple_snapshots(self, engine):
        now = datetime.utcnow()
        for i in range(5):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=5 - i),
                market_cap=10000.0 * (1.05 ** i),
                holder_count=100 + i * 10,
                trading_volume=1000.0 + i * 100,
                price=0.001 * (1.05 ** i),
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.ascension_index > 0
        assert metrics.community_health > 0
        assert metrics.karma_rating > 0
        assert metrics.soul_purity > 0

    def test_metrics_bounds(self, engine):
        now = datetime.utcnow()
        for i in range(10):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=10 - i),
                market_cap=10000.0 * (1.05 ** i),
                holder_count=100 + i * 10,
                trading_volume=1000.0 + i * 100,
                price=0.001 * (1.05 ** i),
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert 0 <= metrics.ascension_index <= 100
        assert 0 <= metrics.community_health <= 100
        assert 0 <= metrics.karma_rating <= 100
        assert 0 <= metrics.soul_purity <= 100
        assert 0 <= metrics.safety_score <= 100

    def test_divine_alignment(self, engine):
        now = datetime.utcnow()
        for i in range(10):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=10 - i),
                market_cap=10000.0 * (1.05 ** i),
                holder_count=100 + i * 10,
                trading_volume=1000.0 + i * 100,
                price=0.001 * (1.05 ** i),
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.divine_alignment in list(DivineAlignment)

    def test_search_by_alignment(self, engine):
        now = datetime.utcnow()
        for j in range(3):
            for i in range(5):
                snapshot = TokenSnapshot(
                    timestamp=now - timedelta(days=5 - i),
                    market_cap=10000.0 * (1.04 ** (i + j)),
                    holder_count=100 + i * 10,
                    trading_volume=1000.0,
                    price=0.001,
                )
                engine.add_snapshot(f"TOKEN{j}", snapshot)

        results = engine.search_by_alignment(DivineAlignment.STABLE)
        assert isinstance(results, list)

    def test_get_top_ascending(self, engine):
        now = datetime.utcnow()
        for j in range(5):
            for i in range(5):
                snapshot = TokenSnapshot(
                    timestamp=now - timedelta(days=5 - i),
                    market_cap=10000.0 * (1.03 ** (i + j * 0.5)),
                    holder_count=100 + i * 5,
                    trading_volume=1000.0,
                    price=0.001,
                )
                engine.add_snapshot(f"TOKEN{j}", snapshot)

        top = engine.get_top_ascending(3)
        assert len(top) <= 3

    def test_metrics_dict_serialization(self, engine):
        snapshot = TokenSnapshot(
            timestamp=datetime.utcnow(),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        d = metrics.to_dict()
        assert "token" in d
        assert "ascension_index" in d
        assert "divine_alignment" in d

    def test_clear(self, engine):
        snapshot = TokenSnapshot(
            timestamp=datetime.utcnow(),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        engine.add_snapshot("TEST", snapshot)
        assert len(engine.tokens) == 1
        engine.clear()
        assert len(engine.tokens) == 0
