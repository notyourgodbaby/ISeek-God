export enum DivineAlignment {
    ENLIGHTENED = "enlightened",
    ASCENDING = "ascending",
    GROWING = "growing",
    STABLE = "stable",
    DESCENDING = "descending",
    LOST = "lost",
}

export interface TokenSnapshot {
    timestamp: number;
    marketCap: number;
    holderCount: number;
    tradingVolume: number;
    price: number;
}

export interface AscensionMetrics {
    tokenName: string;
    currentMarketCap: number;
    ascensionIndex: number;
    communityHealth: number;
    karmaRating: number;
    soulPurity: number;
    divineAlignment: DivineAlignment;
    growthVelocity: number;
    holderVelocity: number;
    safetyScore: number;
}

export class AscensionEngine {
    private tokens: Map<string, TokenSnapshot[]> = new Map();

    addSnapshot(token: string, snapshot: TokenSnapshot): void {
        if (!this.tokens.has(token)) {
            this.tokens.set(token, []);
        }
        this.tokens.get(token)!.push(snapshot);
    }

    analyzeToken(token: string): AscensionMetrics | null {
        const snapshots = this.tokens.get(token);
        if (!snapshots || snapshots.length === 0) {
            return null;
        }

        const sorted = [...snapshots].sort((a, b) => a.timestamp - b.timestamp);
        const latest = sorted[sorted.length - 1];

        let growthVelocity = 0;
        let holderVelocity = 0;

        if (sorted.length > 1) {
            const days = Math.max(1, Math.floor((latest.timestamp - sorted[0].timestamp) / 86400000));
            growthVelocity = ((latest.marketCap - sorted[0].marketCap) / sorted[0].marketCap / days) * 100;
            holderVelocity = (latest.holderCount - sorted[0].holderCount) / days;
        }

        const ascensionIndex = this.calcAscension(sorted);
        const communityHealth = this.calcHealth(sorted);
        const karmaRating = this.calcKarma(sorted);
        const soulPurity = this.calcPurity(sorted);
        const safetyScore = (ascensionIndex + communityHealth + karmaRating) / 3;
        const alignment = this.getAlignment(ascensionIndex);

        return {
            tokenName: token,
            currentMarketCap: latest.marketCap,
            ascensionIndex,
            communityHealth,
            karmaRating,
            soulPurity,
            divineAlignment: alignment,
            growthVelocity,
            holderVelocity,
            safetyScore,
        };
    }

    getTop(limit: number = 10): AscensionMetrics[] {
        const results: AscensionMetrics[] = [];
        for (const token of this.tokens.keys()) {
            const m = this.analyzeToken(token);
            if (m) results.push(m);
        }
        return results
            .sort((a, b) => b.ascensionIndex - a.ascensionIndex)
            .slice(0, limit);
    }

    clear(): void {
        this.tokens.clear();
    }

    private calcAscension(snapshots: TokenSnapshot[]): number {
        if (snapshots.length < 2) return 50.0;
        const growth = Math.min(((snapshots[snapshots.length - 1].marketCap / snapshots[0].marketCap) - 1) * 100, 300);
        const growthScore = Math.min(growth / 3, 100);

        const avg = snapshots.reduce((s, a) => s + a.marketCap, 0) / snapshots.length;
        const variance = snapshots.reduce((s, a) => s + (a.marketCap - avg) ** 2, 0) / snapshots.length;
        const stdDev = Math.sqrt(variance) / avg;
        const consistency = Math.max(0, 100 - stdDev * 50);

        return growthScore * 0.6 + consistency * 0.4;
    }

    private calcHealth(snapshots: TokenSnapshot[]): number {
        if (snapshots.length < 2) return 50.0;
        const holderGrowth = (snapshots[snapshots.length - 1].holderCount - snapshots[0].holderCount) / Math.max(snapshots[0].holderCount, 1) * 100;
        const holderScore = Math.min(holderGrowth / 2, 100);

        const avgVol = snapshots.reduce((s, a) => s + a.tradingVolume, 0) / snapshots.length;
        const healthy = avgVol > 100000 ? 1.0 : 0.5;

        return Math.min(holderScore * 0.7 + healthy * 30, 100);
    }

    private calcKarma(snapshots: TokenSnapshot[]): number {
        if (snapshots.length < 2) return 50.0;
        const changes: number[] = [];
        for (let i = 1; i < snapshots.length; i++) {
            changes.push(Math.abs((snapshots[i].marketCap - snapshots[i - 1].marketCap) / snapshots[i - 1].marketCap) * 100);
        }
        const avg = changes.reduce((a, b) => a + b, 0) / changes.length;
        return Math.max(0, 100 - avg);
    }

    private calcPurity(snapshots: TokenSnapshot[]): number {
        if (snapshots.length < 3) return 50.0;
        const prices = snapshots.map(s => s.price);
        let spikes = 0;
        for (let i = 1; i < prices.length - 1; i++) {
            if (prices[i] > prices[i - 1] * 1.3 && prices[i + 1] < prices[i] * 0.8) {
                spikes++;
            }
        }
        return Math.max(0, 100 - (spikes / Math.max(prices.length - 2, 1)) * 100);
    }

    private getAlignment(idx: number): DivineAlignment {
        if (idx >= 90) return DivineAlignment.ENLIGHTENED;
        if (idx >= 75) return DivineAlignment.ASCENDING;
        if (idx >= 60) return DivineAlignment.GROWING;
        if (idx >= 40) return DivineAlignment.STABLE;
        if (idx >= 20) return DivineAlignment.DESCENDING;
        return DivineAlignment.LOST;
    }
}
