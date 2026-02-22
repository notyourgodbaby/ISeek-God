package main

import (
	"fmt"
	"math"
	"os"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		printHelp()
		return
	}

	command := os.Args[1]

	switch command {
	case "analyze":
		if len(os.Args) < 3 {
			fmt.Println("Usage: iseekgod analyze <token>")
			return
		}
		analyzeToken(os.Args[2])
	case "help":
		printHelp()
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printHelp()
	}
}

func analyzeToken(tokenName string) {
	engine := NewEngine()

	// Add sample data
	now := time.Now()
	for i := 0; i < 10; i++ {
		mc := 10000.0 * math.Pow(1.05, float64(i))
		holders := int(100.0 * math.Pow(1.03, float64(i)))
		volume := mc * 0.1
		price := 0.001 * math.Pow(1.04, float64(i))

		snapshot := TokenSnapshot{
			Timestamp:     now.AddDate(0, 0, -(10-i)),
			MarketCap:     mc,
			HolderCount:   holders,
			TradingVolume: volume,
			Price:         price,
		}
		engine.AddSnapshot(tokenName, snapshot)
	}

	metrics := engine.AnalyzeToken(tokenName)
	if metrics == nil {
		fmt.Printf("Token not found: %s\n", tokenName)
		return
	}

	fmt.Printf("\n╔═════════════════════════════════════════╗\n")
	fmt.Printf("║  Token: %s\n", tokenName)
	fmt.Printf("╚═════════════════════════════════════════╝\n\n")
	fmt.Printf("Ascension Index:   %6.2f/100\n", metrics.AscensionIndex)
	fmt.Printf("Community Health:  %6.2f/100\n", metrics.CommunityHealth)
	fmt.Printf("Karma Rating:      %6.2f/100\n", metrics.KarmaRating)
	fmt.Printf("Soul Purity:       %6.2f/100\n", metrics.SoulPurity)
	fmt.Printf("Safety Score:      %6.2f/100\n\n", metrics.SafetyScore)
	fmt.Printf("Divine Alignment:  %s\n\n", metrics.DivineAlignment)
}

func printHelp() {
	fmt.Println(`
ISeekGod - Token Ascension Engine

COMMANDS:
  analyze <token>    Analyze a token
  help               Show help

EXAMPLE:
  iseekgod analyze DIVINE
`)
}
