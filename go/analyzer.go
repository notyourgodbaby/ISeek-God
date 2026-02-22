package main

import (
	"math"
	"sort"
	"time"
)

func (e *Engine) AnalyzeToken(token string) *AscensionMetrics {
	snapshots, exists := e.tokens[token]
	if !exists || len(snapshots) == 0 {
		return nil
	}

	sort.Slice(snapshots, func(i, j int) bool {
		return snapshots[i].Timestamp.Before(snapshots[j].Timestamp)
	})

	latest := snapshots[len(snapshots)-1]

	var growthVelocity, holderVelocity float64
	if len(snapshots) > 1 {
		daysElapsed := int(latest.Timestamp.Sub(snapshots[0].Timestamp).Hours() / 24)
		if daysElapsed == 0 {
			daysElapsed = 1
		}
		growthVelocity = ((latest.MarketCap - snapshots[0].MarketCap) / snapshots[0].MarketCap) / float64(daysElapsed) * 100
		holderVelocity = float64(latest.HolderCount-snapshots[0].HolderCount) / float64(daysElapsed)
	}

	ascensionIndex := e.calculateAscensionIndex(snapshots)
	communityHealth := e.calculateCommunityHealth(snapshots)
	karmaRating := e.calculateKarmaRating(snapshots)
	soulPurity := e.calculateSoulPurity(snapshots)
	safetyScore := (ascensionIndex + communityHealth + karmaRating) / 3
	alignment := e.getDivineAlignment(ascensionIndex)

	metrics := &AscensionMetrics{
		TokenName:        token,
		CurrentMarketCap: latest.MarketCap,
		AscensionIndex:   ascensionIndex,
		CommunityHealth:  communityHealth,
		KarmaRating:      karmaRating,
		SoulPurity:       soulPurity,
		DivineAlignment:  alignment,
		GrowthVelocity:   growthVelocity,
		HolderVelocity:   holderVelocity,
		SafetyScore:      safetyScore,
		Timestamp:        time.Now(),
	}

	return metrics
}

func (e *Engine) calculateAscensionIndex(snapshots []TokenSnapshot) float64 {
	if len(snapshots) < 2 {
		return 50.0
	}

	totalGrowth := (snapshots[len(snapshots)-1].MarketCap/snapshots[0].MarketCap - 1) * 100
	if totalGrowth > 300 {
		totalGrowth = 300
	}
	growthScore := math.Min(totalGrowth/3, 100)

	var sum float64
	for _, s := range snapshots {
		sum += s.MarketCap
	}
	avg := sum / float64(len(snapshots))

	var variance float64
	for _, s := range snapshots {
		variance += (s.MarketCap - avg) * (s.MarketCap - avg)
	}
	variance /= float64(len(snapshots))
	stdDev := math.Sqrt(variance) / avg
	consistency := math.Max(0, 100-stdDev*50)

	return growthScore*0.6 + consistency*0.4
}

func (e *Engine) calculateCommunityHealth(snapshots []TokenSnapshot) float64 {
	if len(snapshots) < 2 {
		return 50.0
	}

	holderGrowth := float64(snapshots[len(snapshots)-1].HolderCount-snapshots[0].HolderCount) / float64(max(snapshots[0].HolderCount, 1)) * 100
	holderScore := math.Min(holderGrowth/2, 100)

	var sumVolume float64
	for _, s := range snapshots {
		sumVolume += s.TradingVolume
	}
	avgVolume := sumVolume / float64(len(snapshots))
	healthyVolume := 1.0
	if avgVolume <= 100000 {
		healthyVolume = 0.5
	}

	return math.Min(holderScore*0.7+healthyVolume*30, 100)
}

func (e *Engine) calculateKarmaRating(snapshots []TokenSnapshot) float64 {
	if len(snapshots) < 2 {
		return 50.0
	}

	var dailyChanges []float64
	for i := 1; i < len(snapshots); i++ {
		prevMC := snapshots[i-1].MarketCap
		currMC := snapshots[i].MarketCap
		dailyChange := math.Abs((currMC-prevMC)/prevMC) * 100
		dailyChanges = append(dailyChanges, dailyChange)
	}

	if len(dailyChanges) == 0 {
		return 50.0
	}

	var sumVolatility float64
	for _, dc := range dailyChanges {
		sumVolatility += dc
	}
	avgVolatility := sumVolatility / float64(len(dailyChanges))
	return math.Max(0, 100-avgVolatility)
}

func (e *Engine) calculateSoulPurity(snapshots []TokenSnapshot) float64 {
	if len(snapshots) < 3 {
		return 50.0
	}

	prices := make([]float64, len(snapshots))
	for i, s := range snapshots {
		prices[i] = s.Price
	}

	spikeCount := 0
	for i := 1; i < len(prices)-1; i++ {
		prevPrice := prices[i-1]
		currPrice := prices[i]
		nextPrice := prices[i+1]

		if currPrice > prevPrice*1.3 && nextPrice < currPrice*0.8 {
			spikeCount++
		}
	}

	spikeRatio := float64(spikeCount) / float64(max(len(prices)-2, 1))
	return math.Max(0, 100-spikeRatio*100)
}

func (e *Engine) getDivineAlignment(ascensionIndex float64) DivineAlignment {
	if ascensionIndex >= 90 {
		return Enlightened
	} else if ascensionIndex >= 75 {
		return Ascending
	} else if ascensionIndex >= 60 {
		return Growing
	} else if ascensionIndex >= 40 {
		return Stable
	} else if ascensionIndex >= 20 {
		return Descending
	}
	return Lost
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
