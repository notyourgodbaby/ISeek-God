"""
ISeekGod - Token Ascension Engine
Analyze token growth trajectories through divine metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import math


class DivineAlignment(Enum):
    """Token alignment with divine ascension."""
    ENLIGHTENED = "enlightened"  # 90-100
    ASCENDING = "ascending"      # 75-89
    GROWING = "growing"          # 60-74
    STABLE = "stable"            # 40-59
    DESCENDING = "descending"    # 20-39
    LOST = "lost"                # 0-19


@dataclass
class TokenSnapshot:
    """Single point-in-time token metrics."""
    timestamp: datetime
    market_cap: float
    holder_count: int
    trading_volume: float
    price: float


@dataclass
class AscensionMetrics:
    """Complete token ascension analysis."""
    token_name: str
    current_market_cap: float
    ascension_index: float
    community_health: float
    karma_rating: float
    soul_purity: float
    divine_alignment: DivineAlignment
    growth_velocity: float
    holder_velocity: float
    safety_score: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "token": self.token_name,
            "market_cap": self.current_market_cap,
            "ascension_index": round(self.ascension_index, 2),
            "community_health": round(self.community_health, 2),
            "karma_rating": round(self.karma_rating, 2),
            "soul_purity": round(self.soul_purity, 2),
            "divine_alignment": self.divine_alignment.value,
            "growth_velocity": round(self.growth_velocity, 4),
            "holder_velocity": round(self.holder_velocity, 2),
            "safety_score": round(self.safety_score, 2),
            "timestamp": self.timestamp.isoformat(),
        }


class AscensionEngine:
    """Analyze token ascension trajectories."""

    def __init__(self):
        self.tokens = {}
        self.history = {}

    def add_snapshot(self, token: str, snapshot: TokenSnapshot) -> None:
        """Record token snapshot."""
        if token not in self.tokens:
            self.tokens[token] = []
            self.history[token] = []
        self.tokens[token].append(snapshot)

    def analyze_token(self, token: str) -> Optional[AscensionMetrics]:
        """Analyze token ascension metrics."""
        if token not in self.tokens or not self.tokens[token]:
            return None

        snapshots = sorted(self.tokens[token], key=lambda s: s.timestamp)
        latest = snapshots[-1]

        # Calculate velocities
        if len(snapshots) > 1:
            days_elapsed = (latest.timestamp - snapshots[0].timestamp).days
            if days_elapsed == 0:
                days_elapsed = 1

            growth_velocity = (
                ((latest.market_cap - snapshots[0].market_cap) / snapshots[0].market_cap)
                / days_elapsed
                * 100
            )
            holder_velocity = (
                (latest.holder_count - snapshots[0].holder_count) / days_elapsed
            )
        else:
            growth_velocity = 0
            holder_velocity = 0

        ascension_index = self._calculate_ascension_index(snapshots)
        community_health = self._calculate_community_health(snapshots)
        karma_rating = self._calculate_karma_rating(snapshots)
        soul_purity = self._calculate_soul_purity(snapshots)
        safety_score = (ascension_index + community_health + karma_rating) / 3
        alignment = self._get_divine_alignment(ascension_index)

        return AscensionMetrics(
            token_name=token,
            current_market_cap=latest.market_cap,
            ascension_index=ascension_index,
            community_health=community_health,
            karma_rating=karma_rating,
            soul_purity=soul_purity,
            divine_alignment=alignment,
            growth_velocity=growth_velocity,
            holder_velocity=holder_velocity,
            safety_score=safety_score,
        )

    def _calculate_ascension_index(self, snapshots: list) -> float:
        """Calculate ascension index (0-100)."""
        if len(snapshots) < 2:
            return 50.0

        total_growth = (snapshots[-1].market_cap / snapshots[0].market_cap - 1) * 100
        total_growth = min(total_growth, 300)
        growth_score = min(total_growth / 3, 100)

        mc_values = [s.market_cap for s in snapshots]
        avg = sum(mc_values) / len(mc_values)
        variance = sum((x - avg) ** 2 for x in mc_values) / len(mc_values)
        std_dev = math.sqrt(variance) / avg if avg > 0 else 0
        consistency = max(0, 100 - std_dev * 50)

        return (growth_score * 0.6 + consistency * 0.4)

    def _calculate_community_health(self, snapshots: list) -> float:
        """Calculate community health (0-100)."""
        if len(snapshots) < 2:
            return 50.0

        holder_growth = (
            (snapshots[-1].holder_count - snapshots[0].holder_count)
            / max(snapshots[0].holder_count, 1)
        ) * 100
        holder_score = min(holder_growth / 2, 100)

        volumes = [s.trading_volume for s in snapshots]
        avg_volume = sum(volumes) / len(volumes)
        healthy_volume = 1 if avg_volume > 100000 else 0.5

        return min((holder_score * 0.7 + healthy_volume * 30), 100)

    def _calculate_karma_rating(self, snapshots: list) -> float:
        """Calculate karma (sustainability) (0-100)."""
        if len(snapshots) < 2:
            return 50.0

        daily_changes = []
        for i in range(1, len(snapshots)):
            prev_mc = snapshots[i - 1].market_cap
            curr_mc = snapshots[i].market_cap
            daily_change = abs((curr_mc - prev_mc) / prev_mc) * 100
            daily_changes.append(daily_change)

        if daily_changes:
            avg_volatility = sum(daily_changes) / len(daily_changes)
            karma = max(0, 100 - avg_volatility)
        else:
            karma = 50

        return karma

    def _calculate_soul_purity(self, snapshots: list) -> float:
        """Calculate soul purity (pump resistance) (0-100)."""
        if len(snapshots) < 3:
            return 50.0

        prices = [s.price for s in snapshots]
        spike_count = 0

        for i in range(1, len(prices) - 1):
            prev_price = prices[i - 1]
            curr_price = prices[i]
            next_price = prices[i + 1]

            if (curr_price > prev_price * 1.3) and (next_price < curr_price * 0.8):
                spike_count += 1

        spike_ratio = spike_count / max(len(prices) - 2, 1)
        purity = max(0, 100 - spike_ratio * 100)

        return purity

    def _get_divine_alignment(self, ascension_index: float) -> DivineAlignment:
        """Determine divine alignment level."""
        if ascension_index >= 90:
            return DivineAlignment.ENLIGHTENED
        elif ascension_index >= 75:
            return DivineAlignment.ASCENDING
        elif ascension_index >= 60:
            return DivineAlignment.GROWING
        elif ascension_index >= 40:
            return DivineAlignment.STABLE
        elif ascension_index >= 20:
            return DivineAlignment.DESCENDING
        else:
            return DivineAlignment.LOST

    def search_by_alignment(self, alignment: DivineAlignment) -> list:
        """Find tokens by divine alignment."""
        results = []
        for token in self.tokens:
            metrics = self.analyze_token(token)
            if metrics and metrics.divine_alignment == alignment:
                results.append(metrics)
        return sorted(results, key=lambda m: m.ascension_index, reverse=True)

    def get_top_ascending(self, limit: int = 10) -> list:
        """Get top ascending tokens."""
        all_metrics = [
            self.analyze_token(token)
            for token in self.tokens
            if self.analyze_token(token)
        ]
        return sorted(
            all_metrics, key=lambda m: m.ascension_index, reverse=True
        )[:limit]

    def clear(self) -> None:
        """Clear all data."""
        self.tokens = {}
        self.history = {}


class MockEngine(AscensionEngine):
    """Mock engine for testing."""

    def add_mock_token(self, token: str, snapshots_count: int) -> None:
        """Generate mock token data."""
        from datetime import timedelta
        base_mc = 10000.0
        base_holders = 100
        base_price = 0.001

        for i in range(snapshots_count):
            mc = base_mc * (1.05 ** i)
            holders = int(base_holders * (1.03 ** i))
            volume = mc * 0.1 * (1 + (i % 3) * 0.5)
            price = base_price * (1.04 ** i)

            snapshot = TokenSnapshot(
                timestamp=datetime.utcnow() - timedelta(days=snapshots_count - i),
                market_cap=mc,
                holder_count=holders,
                trading_volume=volume,
                price=price,
            )
            self.add_snapshot(token, snapshot)
