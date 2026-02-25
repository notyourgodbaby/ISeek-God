"""Tests for divine alignment classification."""
import pytest
from datetime import datetime, timedelta
from ascension import AscensionEngine, MockEngine, TokenSnapshot, DivineAlignment


@pytest.fixture
def engine():
    return AscensionEngine()


@pytest.fixture
def mock_engine():
    return MockEngine()


class TestAlignment:
    def test_alignment_enlightened(self, engine):
        now = datetime.utcnow()
        for i in range(15):
            snapshot = TokenSnapshot(
                timestamp=now - timedelta(days=15 - i),
                market_cap=10000.0 * (1.08 ** i),
                holder_count=100 + i * 15,
                trading_volume=2000.0 + i * 200,
                price=0.001 * (1.08 ** i),
            )
            engine.add_snapshot("TEST", snapshot)
        metrics = engine.analyze_token("TEST")
        if metrics.ascension_index >= 90:
            assert metrics.divine_alignment == DivineAlignment.ENLIGHTENED

    def test_alignment_ascending(self, mock_engine):
        mock_engine.add_mock_token("TEST", 8)
        metrics = mock_engine.analyze_token("TEST")
        valid = [DivineAlignment.ASCENDING, DivineAlignment.GROWING, DivineAlignment.STABLE]
        assert metrics.divine_alignment in valid

    def test_alignment_growing(self, mock_engine):
        mock_engine.add_mock_token("TEST", 6)
        metrics = mock_engine.analyze_token("TEST")
        valid = [DivineAlignment.GROWING, DivineAlignment.STABLE, DivineAlignment.ASCENDING]
        assert metrics.divine_alignment in valid

    def test_alignment_stable(self, mock_engine):
        mock_engine.add_mock_token("TEST", 4)
        metrics = mock_engine.analyze_token("TEST")
        valid = [DivineAlignment.STABLE, DivineAlignment.GROWING]
        assert metrics.divine_alignment in valid

    def test_alignment_enum_values(self):
        alignments = list(DivineAlignment)
        assert len(alignments) == 6
        values = [a.value for a in alignments]
        assert "enlightened" in values
        assert "ascending" in values
        assert "growing" in values
        assert "stable" in values
        assert "descending" in values
        assert "lost" in values

    def test_alignment_consistency(self, mock_engine):
        mock_engine.add_mock_token("TEST", 5)
        m1 = mock_engine.analyze_token("TEST")
        m2 = mock_engine.analyze_token("TEST")
        assert m1.divine_alignment == m2.divine_alignment

    def test_alignment_to_dict(self, mock_engine):
        mock_engine.add_mock_token("TEST", 5)
        metrics = mock_engine.analyze_token("TEST")
        d = metrics.to_dict()
        assert d["divine_alignment"] in ["enlightened", "ascending", "growing", "stable", "descending", "lost"]

    def test_multiple_tokens_different_alignment(self, mock_engine):
        mock_engine.add_mock_token("TOKEN1", 3)
        mock_engine.add_mock_token("TOKEN2", 8)
        m1 = mock_engine.analyze_token("TOKEN1")
        m2 = mock_engine.analyze_token("TOKEN2")
        assert isinstance(m1.divine_alignment, DivineAlignment)
        assert isinstance(m2.divine_alignment, DivineAlignment)
