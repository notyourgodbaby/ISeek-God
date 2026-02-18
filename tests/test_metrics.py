"""Tests for individual metric calculations."""
import pytest
from datetime import datetime, timedelta
from ascension import AscensionEngine, TokenSnapshot


@pytest.fixture
def engine():
    return AscensionEngine()


class TestMetrics:
    def test_ascension_index_single_snapshot(self, engine):
        snapshot = TokenSnapshot(
            timestamp=datetime.utcnow(),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.ascension_index == 50.0

    def test_ascension_index_growth(self, engine):
        now = datetime.utcnow()
        for i in range(10):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=10 - i),
                market_cap=10000.0 * (1.08 ** i),
                holder_count=100 + i * 10,
                trading_volume=1000.0 + i * 100,
                price=0.001 * (1.08 ** i),
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.ascension_index > 50.0
        assert metrics.ascension_index <= 100

    def test_community_health_holder_growth(self, engine):
        now = datetime.utcnow()
        snapshot1 = TokenSnapshot(
            timestamp=now - timedelta(days=1),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        snapshot2 = TokenSnapshot(
            timestamp=now,
            market_cap=11000.0,
            holder_count=200,
            trading_volume=1100.0,
            price=0.0011,
        )
        engine.add_snapshot("TEST", snapshot1)
        engine.add_snapshot("TEST", snapshot2)
        metrics = engine.analyze_token("TEST")
        assert metrics.community_health > 50.0

    def test_karma_rating_stable(self, engine):
        now = datetime.utcnow()
        for i in range(5):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=5 - i),
                market_cap=10000.0 * (1.02 ** i),
                holder_count=100 + i * 5,
                trading_volume=1000.0,
                price=0.001,
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.karma_rating > 50.0

    def test_karma_rating_volatile(self, engine):
        now = datetime.utcnow()
        snapshots = [
            TokenSnapshot(timestamp=now - timedelta(days=4), market_cap=10000.0, holder_count=100, trading_volume=1000.0, price=0.001),
            TokenSnapshot(timestamp=now - timedelta(days=3), market_cap=15000.0, holder_count=150, trading_volume=1500.0, price=0.0015),
            TokenSnapshot(timestamp=now - timedelta(days=2), market_cap=10500.0, holder_count=105, trading_volume=1050.0, price=0.00105),
            TokenSnapshot(timestamp=now - timedelta(days=1), market_cap=14000.0, holder_count=140, trading_volume=1400.0, price=0.0014),
            TokenSnapshot(timestamp=now, market_cap=11000.0, holder_count=110, trading_volume=1100.0, price=0.0011),
        ]
        for s in snapshots:
            engine.add_snapshot("TEST", s)
        metrics = engine.analyze_token("TEST")
        assert metrics.karma_rating < 80.0

    def test_soul_purity_clean(self, engine):
        now = datetime.utcnow()
        for i in range(5):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=5 - i),
                market_cap=10000.0 * (1.03 ** i),
                holder_count=100 + i * 5,
                trading_volume=1000.0,
                price=0.001 * (1.03 ** i),
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        assert metrics.soul_purity >= 50.0

    def test_safety_score_calculation(self, engine):
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
        expected = (metrics.ascension_index + metrics.community_health + metrics.karma_rating) / 3
        assert abs(metrics.safety_score - expected) < 0.01

    def test_growth_velocity(self, engine):
        now = datetime.utcnow()
        snapshot1 = TokenSnapshot(
            timestamp=now - timedelta(days=10),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        snapshot2 = TokenSnapshot(
            timestamp=now,
            market_cap=12000.0,
            holder_count=120,
            trading_volume=1200.0,
            price=0.0012,
        )
        engine.add_snapshot("TEST", snapshot1)
        engine.add_snapshot("TEST", snapshot2)
        metrics = engine.analyze_token("TEST")
        assert metrics.growth_velocity > 0

    def test_holder_velocity(self, engine):
        now = datetime.utcnow()
        snapshot1 = TokenSnapshot(
            timestamp=now - timedelta(days=5),
            market_cap=10000.0,
            holder_count=100,
            trading_volume=1000.0,
            price=0.001,
        )
        snapshot2 = TokenSnapshot(
            timestamp=now,
            market_cap=10000.0,
            holder_count=150,
            trading_volume=1000.0,
            price=0.001,
        )
        engine.add_snapshot("TEST", snapshot1)
        engine.add_snapshot("TEST", snapshot2)
        metrics = engine.analyze_token("TEST")
        assert metrics.holder_velocity == 10.0
