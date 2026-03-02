use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct TokenSnapshot {
    pub timestamp: u64,
    pub market_cap: f64,
    pub holder_count: u32,
    pub trading_volume: f64,
    pub price: f64,
}

#[derive(Clone, Debug, PartialEq)]
pub enum DivineAlignment {
    Enlightened,
    Ascending,
    Growing,
    Stable,
    Descending,
    Lost,
}

impl DivineAlignment {
    pub fn as_str(&self) -> &'static str {
        match self {
            DivineAlignment::Enlightened => "enlightened",
            DivineAlignment::Ascending => "ascending",
            DivineAlignment::Growing => "growing",
            DivineAlignment::Stable => "stable",
            DivineAlignment::Descending => "descending",
            DivineAlignment::Lost => "lost",
        }
    }
}

#[derive(Clone, Debug)]
pub struct AscensionMetrics {
    pub token_name: String,
    pub current_market_cap: f64,
    pub ascension_index: f64,
    pub community_health: f64,
    pub karma_rating: f64,
    pub soul_purity: f64,
    pub divine_alignment: DivineAlignment,
    pub growth_velocity: f64,
    pub holder_velocity: f64,
    pub safety_score: f64,
}

pub struct AscensionEngine {
    tokens: HashMap<String, Vec<TokenSnapshot>>,
}

impl AscensionEngine {
    pub fn new() -> Self {
        AscensionEngine {
            tokens: HashMap::new(),
        }
    }

    pub fn add_snapshot(&mut self, token: &str, snapshot: TokenSnapshot) {
        self.tokens
            .entry(token.to_string())
            .or_insert_with(Vec::new)
            .push(snapshot);
    }

    pub fn analyze_token(&self, token: &str) -> Option<AscensionMetrics> {
        let snapshots = self.tokens.get(token)?;
        if snapshots.is_empty() {
            return None;
        }

        let mut sorted = snapshots.clone();
        sorted.sort_by(|a, b| a.timestamp.cmp(&b.timestamp));

        let latest = sorted[sorted.len() - 1].clone();

        let (growth_velocity, holder_velocity) = if sorted.len() > 1 {
            let days = (latest.timestamp - sorted[0].timestamp) / 86400;
            let days = if days == 0 { 1 } else { days };
            let growth = ((latest.market_cap - sorted[0].market_cap) / sorted[0].market_cap)
                / days as f64
                * 100.0;
            let holders = (latest.holder_count as i64 - sorted[0].holder_count as i64)
                / days as i64;
            (growth, holders as f64)
        } else {
            (0.0, 0.0)
        };

        let ascension_index = Self::calc_ascension(&sorted);
        let community_health = Self::calc_health(&sorted);
        let karma_rating = Self::calc_karma(&sorted);
        let soul_purity = Self::calc_purity(&sorted);
        let safety_score = (ascension_index + community_health + karma_rating) / 3.0;
        let divine_alignment = Self::get_alignment(ascension_index);

        Some(AscensionMetrics {
            token_name: token.to_string(),
            current_market_cap: latest.market_cap,
            ascension_index,
            community_health,
            karma_rating,
            soul_purity,
            divine_alignment,
            growth_velocity,
            holder_velocity,
            safety_score,
        })
    }

    fn calc_ascension(snapshots: &[TokenSnapshot]) -> f64 {
        if snapshots.len() < 2 {
            return 50.0;
        }
        let growth = ((snapshots[snapshots.len() - 1].market_cap / snapshots[0].market_cap) - 1.0) * 100.0;
        let growth = if growth > 300.0 { 300.0 } else { growth };
        let growth_score = (growth / 3.0).min(100.0);

        let avg = snapshots.iter().map(|s| s.market_cap).sum::<f64>() / snapshots.len() as f64;
        let var = snapshots
            .iter()
            .map(|s| (s.market_cap - avg).powi(2))
            .sum::<f64>()
            / snapshots.len() as f64;
        let std_dev = var.sqrt() / avg;
        let consistency = (100.0 - std_dev * 50.0).max(0.0);

        growth_score * 0.6 + consistency * 0.4
    }

    fn calc_health(snapshots: &[TokenSnapshot]) -> f64 {
        if snapshots.len() < 2 {
            return 50.0;
        }
        let holder_growth = (snapshots[snapshots.len() - 1].holder_count as f64
            - snapshots[0].holder_count as f64)
            / snapshots[0].holder_count.max(1) as f64
            * 100.0;
        let holder_score = (holder_growth / 2.0).min(100.0);

        let avg_vol =
            snapshots.iter().map(|s| s.trading_volume).sum::<f64>() / snapshots.len() as f64;
        let healthy = if avg_vol > 100000.0 { 1.0 } else { 0.5 };

        (holder_score * 0.7 + healthy * 30.0).min(100.0)
    }

    fn calc_karma(snapshots: &[TokenSnapshot]) -> f64 {
        if snapshots.len() < 2 {
            return 50.0;
        }
        let mut changes = Vec::new();
        for i in 1..snapshots.len() {
            let change = ((snapshots[i].market_cap - snapshots[i - 1].market_cap)
                / snapshots[i - 1].market_cap)
                .abs()
                * 100.0;
            changes.push(change);
        }
        if changes.is_empty() {
            return 50.0;
        }
        let avg_vol = changes.iter().sum::<f64>() / changes.len() as f64;
        (100.0 - avg_vol).max(0.0)
    }

    fn calc_purity(snapshots: &[TokenSnapshot]) -> f64 {
        if snapshots.len() < 3 {
            return 50.0;
        }
        let prices: Vec<_> = snapshots.iter().map(|s| s.price).collect();
        let mut spikes = 0;
        for i in 1..prices.len() - 1 {
            if prices[i] > prices[i - 1] * 1.3 && prices[i + 1] < prices[i] * 0.8 {
                spikes += 1;
            }
        }
        let ratio = spikes as f64 / (prices.len() - 2).max(1) as f64;
        (100.0 - ratio * 100.0).max(0.0)
    }

    fn get_alignment(idx: f64) -> DivineAlignment {
        match idx {
            x if x >= 90.0 => DivineAlignment::Enlightened,
            x if x >= 75.0 => DivineAlignment::Ascending,
            x if x >= 60.0 => DivineAlignment::Growing,
            x if x >= 40.0 => DivineAlignment::Stable,
            x if x >= 20.0 => DivineAlignment::Descending,
            _ => DivineAlignment::Lost,
        }
    }

    pub fn get_top(&self, limit: usize) -> Vec<AscensionMetrics> {
        let mut results = Vec::new();
        for token in self.tokens.keys() {
            if let Some(m) = self.analyze_token(token) {
                results.push(m);
            }
        }
        results.sort_by(|a, b| b.ascension_index.partial_cmp(&a.ascension_index).unwrap());
        results.into_iter().take(limit).collect()
    }

    pub fn clear(&mut self) {
        self.tokens.clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        let engine = AscensionEngine::new();
        assert_eq!(engine.tokens.len(), 0);
    }

    #[test]
    fn test_add_snapshot() {
        let mut engine = AscensionEngine::new();
        engine.add_snapshot(
            "TEST",
            TokenSnapshot {
                timestamp: 1000,
                market_cap: 10000.0,
                holder_count: 100,
                trading_volume: 1000.0,
                price: 0.001,
            },
        );
        assert_eq!(engine.tokens.len(), 1);
    }

    #[test]
    fn test_analyze_single() {
        let mut engine = AscensionEngine::new();
        engine.add_snapshot(
            "TEST",
            TokenSnapshot {
                timestamp: 1000,
                market_cap: 10000.0,
                holder_count: 100,
                trading_volume: 1000.0,
                price: 0.001,
            },
        );
        let m = engine.analyze_token("TEST").unwrap();
        assert_eq!(m.token_name, "TEST");
        assert_eq!(m.ascension_index, 50.0);
    }

    #[test]
    fn test_alignment_enlightened() {
        assert_eq!(
            AscensionEngine::get_alignment(95.0),
            DivineAlignment::Enlightened
        );
    }

    #[test]
    fn test_alignment_ascending() {
        assert_eq!(
            AscensionEngine::get_alignment(80.0),
            DivineAlignment::Ascending
        );
    }

    #[test]
    fn test_alignment_growing() {
        assert_eq!(
            AscensionEngine::get_alignment(65.0),
            DivineAlignment::Growing
        );
    }

    #[test]
    fn test_alignment_stable() {
        assert_eq!(
            AscensionEngine::get_alignment(50.0),
            DivineAlignment::Stable
        );
    }

    #[test]
    fn test_alignment_descending() {
        assert_eq!(
            AscensionEngine::get_alignment(25.0),
            DivineAlignment::Descending
        );
    }

    #[test]
    fn test_alignment_lost() {
        assert_eq!(AscensionEngine::get_alignment(5.0), DivineAlignment::Lost);
    }

    #[test]
    fn test_as_str() {
        assert_eq!(DivineAlignment::Enlightened.as_str(), "enlightened");
        assert_eq!(DivineAlignment::Ascending.as_str(), "ascending");
    }

    #[test]
    fn test_growth() {
        let mut engine = AscensionEngine::new();
        for i in 0..5 {
            engine.add_snapshot(
                "TEST",
                TokenSnapshot {
                    timestamp: (i * 86400) as u64,
                    market_cap: 10000.0 * 1.05f64.powi(i),
                    holder_count: 100 + i as u32 * 10,
                    trading_volume: 1000.0,
                    price: 0.001,
                },
            );
        }
        let m = engine.analyze_token("TEST").unwrap();
        assert!(m.ascension_index > 50.0);
    }

    #[test]
    fn test_get_top() {
        let mut engine = AscensionEngine::new();
        for j in 0..3 {
            for i in 0..5 {
                engine.add_snapshot(
                    &format!("TOKEN{}", j),
                    TokenSnapshot {
                        timestamp: (i * 86400) as u64,
                        market_cap: 10000.0,
                        holder_count: 100,
                        trading_volume: 1000.0,
                        price: 0.001,
                    },
                );
            }
        }
        let top = engine.get_top(2);
        assert!(top.len() <= 2);
    }

    #[test]
    fn test_clear() {
        let mut engine = AscensionEngine::new();
        engine.add_snapshot(
            "TEST",
            TokenSnapshot {
                timestamp: 1000,
                market_cap: 10000.0,
                holder_count: 100,
                trading_volume: 1000.0,
                price: 0.001,
            },
        );
        assert_eq!(engine.tokens.len(), 1);
        engine.clear();
        assert_eq!(engine.tokens.len(), 0);
    }

    #[test]
    fn test_bounds() {
        let mut engine = AscensionEngine::new();
        for i in 0..10 {
            engine.add_snapshot(
                "TEST",
                TokenSnapshot {
                    timestamp: (i * 86400) as u64,
                    market_cap: 10000.0 * 1.05f64.powi(i),
                    holder_count: 100 + i as u32 * 10,
                    trading_volume: 1000.0 + i as f64 * 100.0,
                    price: 0.001,
                },
            );
        }
        let m = engine.analyze_token("TEST").unwrap();
        assert!(m.ascension_index >= 0.0 && m.ascension_index <= 100.0);
        assert!(m.community_health >= 0.0 && m.community_health <= 100.0);
        assert!(m.safety_score >= 0.0 && m.safety_score <= 100.0);
    }

    #[test]
    fn test_nonexistent() {
        let engine = AscensionEngine::new();
        assert!(engine.analyze_token("NOTHERE").is_none());
    }
}
