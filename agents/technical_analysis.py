"""
Orin.LAB · Technical Analysis Engine
Pure-Python implementation of core TA indicators.
No external TA libraries — computed from raw OHLCV data.
"""

from __future__ import annotations

import math
import httpx
from dataclasses import dataclass, field
from typing import Optional
from utils.logger import get_logger

logger = get_logger("technical_analysis")


# ──────────────────────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Candle:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class TAResult:
    symbol: str
    price: float
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    bb_width: Optional[float] = None
    bb_pct: Optional[float] = None       # %B — where price is within bands
    ema_9: Optional[float] = None
    ema_21: Optional[float] = None
    ema_50: Optional[float] = None
    sma_200: Optional[float] = None
    volume_sma: Optional[float] = None
    volume_ratio: Optional[float] = None  # current vol / avg vol
    atr: Optional[float] = None
    signal: str = "HOLD"
    confidence: int = 50
    reasons: list[str] = field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────────────
# Core math helpers
# ──────────────────────────────────────────────────────────────────────────────

def _ema(values: list[float], period: int) -> list[float]:
    """Exponential Moving Average — full series."""
    if len(values) < period:
        return []
    k = 2.0 / (period + 1)
    result = [sum(values[:period]) / period]
    for v in values[period:]:
        result.append(v * k + result[-1] * (1 - k))
    return result


def _sma(values: list[float], period: int) -> list[float]:
    """Simple Moving Average — full series."""
    return [
        sum(values[i:i + period]) / period
        for i in range(len(values) - period + 1)
    ]


def _stdev(values: list[float]) -> float:
    """Population standard deviation."""
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))


# ──────────────────────────────────────────────────────────────────────────────
# Indicators
# ──────────────────────────────────────────────────────────────────────────────

def rsi(closes: list[float], period: int = 14) -> Optional[float]:
    """
    Relative Strength Index (Wilder smoothing).
    Returns value in [0, 100]. >70 overbought, <30 oversold.
    """
    if len(closes) < period + 1:
        return None

    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(d, 0.0) for d in deltas]
    losses = [abs(min(d, 0.0)) for d in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def macd(
    closes: list[float],
    fast: int = 12,
    slow: int = 26,
    signal_period: int = 9,
) -> tuple[Optional[float], Optional[float], Optional[float]]:
    """
    MACD — returns (macd_line, signal_line, histogram).
    """
    if len(closes) < slow + signal_period:
        return None, None, None

    ema_fast = _ema(closes, fast)
    ema_slow = _ema(closes, slow)

    # Align series lengths
    offset = len(ema_fast) - len(ema_slow)
    macd_line = [f - s for f, s in zip(ema_fast[offset:], ema_slow)]

    if len(macd_line) < signal_period:
        return None, None, None

    sig_line = _ema(macd_line, signal_period)
    hist = macd_line[-1] - sig_line[-1]

    return round(macd_line[-1], 6), round(sig_line[-1], 6), round(hist, 6)


def bollinger_bands(
    closes: list[float],
    period: int = 20,
    num_std: float = 2.0,
) -> tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Bollinger Bands — returns (upper, middle, lower).
    """
    if len(closes) < period:
        return None, None, None

    window = closes[-period:]
    middle = sum(window) / period
    std = _stdev(window)
    return (
        round(middle + num_std * std, 6),
        round(middle, 6),
        round(middle - num_std * std, 6),
    )


def atr(candles: list[Candle], period: int = 14) -> Optional[float]:
    """
    Average True Range — measures volatility.
    """
    if len(candles) < period + 1:
        return None

    trs = []
    for i in range(1, len(candles)):
        high = candles[i].high
        low = candles[i].low
        prev_close = candles[i - 1].close
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)

    if len(trs) < period:
        return None

    # Wilder smoothing
    atr_val = sum(trs[:period]) / period
    for tr in trs[period:]:
        atr_val = (atr_val * (period - 1) + tr) / period

    return round(atr_val, 6)


# ──────────────────────────────────────────────────────────────────────────────
# Signal generation from indicators
# ──────────────────────────────────────────────────────────────────────────────

def _score_rsi(rsi_val: float, reasons: list[str]) -> int:
    """Return score delta from RSI."""
    if rsi_val < 30:
        reasons.append(f"RSI {rsi_val:.1f} — oversold (bullish)")
        return 15
    if rsi_val < 40:
        reasons.append(f"RSI {rsi_val:.1f} — approaching oversold")
        return 7
    if rsi_val > 70:
        reasons.append(f"RSI {rsi_val:.1f} — overbought (bearish)")
        return -15
    if rsi_val > 60:
        reasons.append(f"RSI {rsi_val:.1f} — approaching overbought")
        return -7
    return 0


def _score_macd(macd_val: float, hist: float, reasons: list[str]) -> int:
    """Return score delta from MACD."""
    score = 0
    if macd_val > 0:
        reasons.append("MACD above signal — bullish momentum")
        score += 10
    else:
        reasons.append("MACD below signal — bearish momentum")
        score -= 10
    if hist > 0:
        score += 5
    else:
        score -= 5
    return score


def _score_bb(price: float, upper: float, middle: float, lower: float, reasons: list[str]) -> int:
    """Return score delta from Bollinger Bands position."""
    pct_b = (price - lower) / (upper - lower) if upper != lower else 0.5
    if pct_b < 0.1:
        reasons.append("Price near lower Bollinger Band — potential reversal")
        return 12
    if pct_b > 0.9:
        reasons.append("Price near upper Bollinger Band — potential resistance")
        return -12
    if pct_b < 0.3:
        reasons.append("Price in lower BB zone")
        return 5
    if pct_b > 0.7:
        reasons.append("Price in upper BB zone")
        return -5
    return 0


def _score_ema_trend(price: float, ema9: float, ema21: float, ema50: float, reasons: list[str]) -> int:
    """Return score delta from EMA alignment."""
    score = 0
    if price > ema9 > ema21 > ema50:
        reasons.append("Price above all EMAs — strong uptrend")
        score += 15
    elif price < ema9 < ema21 < ema50:
        reasons.append("Price below all EMAs — strong downtrend")
        score -= 15
    elif price > ema21:
        reasons.append("Price above EMA 21 — moderate bullish")
        score += 7
    elif price < ema21:
        reasons.append("Price below EMA 21 — moderate bearish")
        score -= 7
    return score


def _score_volume(ratio: float, reasons: list[str]) -> int:
    """Return score delta from volume vs average."""
    if ratio > 2.0:
        reasons.append(f"Volume {ratio:.1f}x above average — high conviction")
        return 8
    if ratio > 1.5:
        reasons.append(f"Volume {ratio:.1f}x above average")
        return 4
    if ratio < 0.5:
        reasons.append("Low volume — weak conviction")
        return -4
    return 0


def compute_signal(result: TAResult) -> TAResult:
    """
    Aggregate indicator scores into a final BUY/SELL/HOLD signal.
    Score range: -100 to +100.
    """
    score = 0

    if result.rsi is not None:
        score += _score_rsi(result.rsi, result.reasons)

    if result.macd is not None and result.macd_histogram is not None:
        score += _score_macd(result.macd, result.macd_histogram, result.reasons)

    if result.bb_upper is not None:
        score += _score_bb(result.price, result.bb_upper, result.bb_middle, result.bb_lower, result.reasons)

    if result.ema_9 is not None and result.ema_21 is not None and result.ema_50 is not None:
        score += _score_ema_trend(result.price, result.ema_9, result.ema_21, result.ema_50, result.reasons)

    if result.volume_ratio is not None:
        score += _score_volume(result.volume_ratio, result.reasons)

    # Map score → signal + confidence
    if score >= 20:
        result.signal = "BUY"
        result.confidence = min(50 + score, 95)
    elif score <= -20:
        result.signal = "SELL"
        result.confidence = min(50 + abs(score), 95)
    else:
        result.signal = "HOLD"
        result.confidence = max(40, 60 - abs(score))

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Data fetcher — CoinGecko OHLCV
# ──────────────────────────────────────────────────────────────────────────────

COINGECKO_IDS = {
    "SOL": "solana", "BTC": "bitcoin", "ETH": "ethereum",
    "JUP": "jupiter-exchange-solana", "BONK": "bonk", "WIF": "dogwifcoin",
}


def fetch_ohlcv(symbol: str, days: int = 30) -> list[Candle]:
    """Fetch daily OHLCV from CoinGecko (no API key required)."""
    cg_id = COINGECKO_IDS.get(symbol.upper(), symbol.lower())
    try:
        resp = httpx.get(
            f"https://api.coingecko.com/api/v3/coins/{cg_id}/ohlc",
            params={"vs_currency": "usd", "days": str(days)},
            timeout=15,
        )
        resp.raise_for_status()
        raw = resp.json()
        return [
            Candle(timestamp=r[0], open=r[1], high=r[2], low=r[3], close=r[4], volume=0.0)
            for r in raw
        ]
    except Exception as exc:
        logger.warning(f"OHLCV fetch failed for {symbol}: {exc}")
        return []


def fetch_volume(symbol: str, days: int = 30) -> list[float]:
    """Fetch daily volume from CoinGecko market_chart endpoint."""
    cg_id = COINGECKO_IDS.get(symbol.upper(), symbol.lower())
    try:
        resp = httpx.get(
            f"https://api.coingecko.com/api/v3/coins/{cg_id}/market_chart",
            params={"vs_currency": "usd", "days": str(days), "interval": "daily"},
            timeout=15,
        )
        resp.raise_for_status()
        return [v[1] for v in resp.json().get("total_volumes", [])]
    except Exception:
        return []


# ──────────────────────────────────────────────────────────────────────────────
# Main public API
# ──────────────────────────────────────────────────────────────────────────────

def analyze(symbol: str) -> TAResult:
    """
    Full TA analysis for a symbol.
    Fetches OHLCV data and computes all indicators.
    """
    candles = fetch_ohlcv(symbol, days=60)
    volumes = fetch_volume(symbol, days=30)

    if not candles:
        return TAResult(symbol=symbol, price=0.0, signal="HOLD", confidence=0,
                        reasons=["No price data available"])

    closes = [c.close for c in candles]
    price = closes[-1]
    result = TAResult(symbol=symbol, price=price)

    # RSI
    result.rsi = rsi(closes)

    # MACD
    result.macd, result.macd_signal, result.macd_histogram = macd(closes)

    # Bollinger Bands
    result.bb_upper, result.bb_middle, result.bb_lower = bollinger_bands(closes)
    if result.bb_upper and result.bb_lower and result.bb_upper != result.bb_lower:
        result.bb_width = round((result.bb_upper - result.bb_lower) / result.bb_middle * 100, 2)
        result.bb_pct = round((price - result.bb_lower) / (result.bb_upper - result.bb_lower), 3)

    # EMAs
    ema9_series  = _ema(closes, 9)
    ema21_series = _ema(closes, 21)
    ema50_series = _ema(closes, 50)
    if ema9_series:  result.ema_9  = round(ema9_series[-1], 4)
    if ema21_series: result.ema_21 = round(ema21_series[-1], 4)
    if ema50_series: result.ema_50 = round(ema50_series[-1], 4)

    # SMA 200
    sma200 = _sma(closes, 200)
    if sma200: result.sma_200 = round(sma200[-1], 4)

    # ATR
    result.atr = atr(candles)

    # Volume
    if volumes:
        avg_vol = sum(volumes[:-1]) / max(len(volumes) - 1, 1)
        if avg_vol > 0:
            result.volume_sma = round(avg_vol, 2)
            result.volume_ratio = round(volumes[-1] / avg_vol, 2)

    return compute_signal(result)


def format_report(result: TAResult) -> str:
    """Format TAResult as a readable terminal/Telegram report."""
    sig_emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡"}.get(result.signal, "⚪")
    lines = [
        f"📊 *{result.symbol} Technical Analysis*",
        f"Price: ${result.price:,.4f}",
        "",
        f"{sig_emoji} *SIGNAL: {result.signal}* | Confidence: {result.confidence}/100",
        "",
        "*Indicators:*",
    ]
    if result.rsi is not None:
        lines.append(f"  RSI(14): {result.rsi:.1f}")
    if result.macd is not None:
        lines.append(f"  MACD: {result.macd:.6f} | Hist: {result.macd_histogram:.6f}")
    if result.bb_upper is not None:
        lines.append(f"  BB: {result.bb_lower:.4f} — {result.bb_upper:.4f} | %B: {result.bb_pct:.2f}")
    if result.ema_9:
        lines.append(f"  EMA(9/21/50): {result.ema_9:.4f} / {result.ema_21:.4f} / {result.ema_50:.4f}")
    if result.atr:
        lines.append(f"  ATR(14): {result.atr:.4f}")
    if result.volume_ratio:
        lines.append(f"  Volume: {result.volume_ratio:.2f}x avg")
    if result.reasons:
        lines.append("")
        lines.append("*Reasons:*")
        for r in result.reasons:
            lines.append(f"  • {r}")
    return "\n".join(lines)
