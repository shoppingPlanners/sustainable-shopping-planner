#!/usr/bin/env python3
"""
Run the Brand Data Collector to scrape real sustainable fashion products.

This script will:
1. Read the websites.txt file for target URLs
2. Scrape product data from each configured sustainable fashion brand
3. Save results to brand_data.json
4. Upload to MongoDB database

Usage:
    python run_collector.py

Note: Please ensure you comply with each website's robots.txt and terms of service.
This tool is for educational purposes and personal use only.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from collector import main

if __name__ == "__main__":
    print("=" * 60)
    print("🌿 SUSTAINABLE FASHION DATA COLLECTOR")
    print("=" * 60)
    print("\n📋 This will scrape product data from 35+ brands:")
    print("\n   🏔️  Major Brands: Patagonia, Reformation, Everlane")
    print("   👟 Footwear: Allbirds, Nisolo, Rothy's, Vivobarefoot")
    print("   👕 Basics: Pact, Kotn, Mate the Label, Organic Basics")
    print("   🏃 Activewear: Girlfriend Collective, Tentree, prAna")
    print("   💎 Luxury: Eileen Fisher, Cuyana, People Tree")
    print("   👜 Accessories: ABLE, Matt & Nat, Angela Roi")
    print("   🌍 Fair Trade: Tradeland, SERRV, Global Goods")
    print("   👖 Denim: AGOLDE, Outland Denim")
    print("   🌱 Vegan: Wuxly, Veerah")
    print("   ♻️  Zero Waste: Tonlé, Christy Martin Design")
    print("   ...and more!")
    print("\n⚠️  Note: Web scraping should respect robots.txt and ToS")
    print("   This tool is for educational purposes only.\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    print("\n🚀 Starting collector...\n")
    main()
    print("\n✅ Collection complete! Check brand_data.json for results.")

