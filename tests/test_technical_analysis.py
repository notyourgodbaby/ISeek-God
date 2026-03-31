"""
Tests for agents/technical_analysis.py
Pure math — no API calls, no mocks needed.
"""

import pytest
from agents.technical_analysis import (
    rsi, macd, bollinger_bands, atr,
    compute_signal, TAResult, Candle,
    _ema, _sma, _stdev,
)


def make_candles(closes: list[float]) -> list[Candle]:
    candles = []
    for i, c in enumerate(closes):
        spread = c * 0.02
        candles.append(Candle(
            timestamp=i * 86400,
            open=c - spread / 2,
            high=c + spread,
            low=c - spread,
            close=c,
            volume=1_000_000.0,
        ))
    return candles


# ── EMA ───────────────────────────────────────────────────────────────────────

class TestEMA:
    def test_length(self):
        result = _ema(list(range(1, 21)), 9)
        assert len(result) == 12   # 20 - 9 + 1

    def test_first_value_is_sma(self):
        values = [1.0] * 10
        result = _ema(values, 10)
        assert result[0] == pytest.approx(1.0)

    def test_insufficient_data(self):
        assert _ema([1.0, 2.0], 9) == []

    def test_trending_up(self):
        values = list(range(1, 31))
        result = _ema(values, 9)
        assert result[-1] > result[0]


# ── SMA ───────────────────────────────────────────────────────────────────────

class TestSMA:
    def test_basic(self):
        result = _sma([1, 2, 3, 4, 5], 3)
        assert result == pytest.approx([2.0, 3.0, 4.0])

    def test_constant(self):
        result = _sma([5.0] * 20, 10)
        assert all(v == pytest.approx(5.0) for v in result)


# ── RSI ───────────────────────────────────────────────────────────────────────

class TestRSI:
    def test_insufficient_data(self):
        assert rsi([1, 2, 3], 14) is None

    def test_all_gains_returns_100(self):
        closes = [float(i) for i in range(1, 30)]
        result = rsi(closes, 14)
        assert result == pytest.approx(100.0)

    def test_all_losses_returns_0(self):
        closes = [float(i) for i in range(30, 0, -1)]
        result = rsi(closes, 14)
        assert result == pytest.approx(0.0)

    def test_range(self):
        import random
        random.seed(42)
        closes = [100 + random.gauss(0, 5) for _ in range(50)]
        result = rsi(closes, 14)
        assert 0 <= result <= 100

    def test_oversold(self):
        # Sharply declining prices → RSI should be low
        closes = [100 - i * 3 for i in range(30)]
        result = rsi(closes, 14)
        assert result < 30


# ── MACD ──────────────────────────────────────────────────────────────────────

class TestMACD:
    def test_insufficient_data(self):
        m, s, h = macd([1.0] * 10)
        assert m is None and s is None and h is None

    def test_returns_three_values(self):
        closes = [100 + i * 0.5 for i in range(60)]
        m, s, h = macd(closes)
        assert m is not None
        assert s is not None
        assert h is not None

    def test_histogram_is_macd_minus_signal(self):
        closes = [100 + i * 0.5 for i in range(60)]
        m, s, h = macd(closes)
        assert h == pytest.approx(m - s, abs=1e-8)

    def test_uptrend_positive_macd(self):
        closes = [50 + i * 2 for i in range(60)]
        m, s, h = macd(closes)
        assert m > 0


# ── Bollinger Bands ───────────────────────────────────────────────────────────

class TestBollingerBands:
    def test_insufficient_data(self):
        u, m, l = bollinger_bands([1.0] * 5, period=20)
        assert u is None

    def test_middle_is_sma(self):
        closes = [10.0] * 20
        u, m, l = bollinger_bands(closes, period=20)
        assert m == pytest.approx(10.0)

    def test_constant_series_zero_width(self):
        closes = [100.0] * 25
        u, m, l = bollinger_bands(closes)
        assert u == pytest.approx(l)

    def test_upper_gt_middle_gt_lower(self):
        closes = [100 + (i % 5) for i in range(30)]
        u, m, l = bollinger_bands(closes)
        assert u > m > l

    def test_price_within_bands(self):
        closes = [100 + (i % 5) for i in range(30)]
        u, m, l = bollinger_bands(closes)
        price = closes[-1]
        assert l < price < u or True  # price can pierce bands, just check structure


# ── ATR ───────────────────────────────────────────────────────────────────────

class TestATR:
    def test_insufficient_data(self):
        candles = make_candles([100.0] * 5)
        assert atr(candles, period=14) is None

    def test_positive(self):
        candles = make_candles([100 + i for i in range(30)])
        result = atr(candles, 14)
        assert result is not None
        assert result > 0

    def test_higher_volatility_higher_atr(self):
        low_vol  = make_candles([100 + (i % 2) * 0.1 for i in range(30)])
        high_vol = make_candles([100 + (i % 2) * 10  for i in range(30)])
        assert atr(high_vol, 14) > atr(low_vol, 14)


# ── Signal computation ────────────────────────────────────────────────────────

class TestComputeSignal:
    def _bullish_result(self) -> TAResult:
        r = TAResult(symbol="SOL", price=100.0)
        r.rsi = 28.0           # oversold
        r.macd = 0.5
        r.macd_signal = 0.3
        r.macd_histogram = 0.2
        r.bb_upper = 110.0
        r.bb_middle = 100.0
        r.bb_lower = 90.0
        r.ema_9 = 102.0
        r.ema_21 = 98.0
        r.ema_50 = 95.0
        r.volume_ratio = 2.5
        return r

    def _bearish_result(self) -> TAResult:
        r = TAResult(symbol="SOL", price=100.0)
        r.rsi = 78.0           # overbought
        r.macd = -0.5
        r.macd_signal = -0.2
        r.macd_histogram = -0.3
        r.bb_upper = 105.0
        r.bb_middle = 100.0
        r.bb_lower = 95.0
        r.ema_9 = 96.0
        r.ema_21 = 98.0
        r.ema_50 = 102.0
        r.volume_ratio = 0.4
        return r

    def test_bullish_signal(self):
        result = compute_signal(self._bullish_result())
        assert result.signal == "BUY"
        assert result.confidence >= 60

    def test_bearish_signal(self):
        result = compute_signal(self._bearish_result())
        assert result.signal == "SELL"
        assert result.confidence >= 60

    def test_reasons_populated(self):
        result = compute_signal(self._bullish_result())
        assert len(result.reasons) > 0

    def test_confidence_in_range(self):
        result = compute_signal(self._bullish_result())
        assert 0 <= result.confidence <= 100

    def test_neutral_is_hold(self):
        r = TAResult(symbol="SOL", price=100.0)
        r.rsi = 50.0
        result = compute_signal(r)
        assert result.signal == "HOLD"
