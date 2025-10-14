# collector.py

import json
import logging
from urllib.parse import urlparse
from scraper_agent import CategoryCrawler
from config import SITE_CONFIGS

# --- Configuration ---
WEBSITES_FILE = "websites.txt"
OUTPUT_FILE = "brand_data.json"

# --- Setup Logging ---
# This provides detailed feedback in the terminal about what the script is doing.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_config_for_url(url):
    """Matches a URL to its specific configuration in config.py."""
    domain = urlparse(url).netloc.replace('www.', '')
    if domain in SITE_CONFIGS:
        return SITE_CONFIGS[domain]
    logging.warning(f"No specific configuration for {domain}. Scraper may not work correctly.")
    return None

def main():
    """Main function to run the data collection agent."""
    logging.info("Brand Data Collector Agent: Initializing...")
    try:
        with open(WEBSITES_FILE, "r") as f:
            start_urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"FATAL: The file '{WEBSITES_FILE}' was not found. Please create it.")
        return

    if not start_urls:
        logging.error("FATAL: The 'websites.txt' file is empty. Please add category URLs to it.")
        return

    all_brand_data = []
    for url in start_urls:
        config = get_config_for_url(url)
        if not config:
            continue

        crawler = CategoryCrawler(start_url=url, config=config)
        products = crawler.crawl()
        
        brand_data = {
            "brand_domain": urlparse(url).netloc,
            "source_category_url": url,
            "product_count": len(products),
            "products": products
        }
        all_brand_data.append(brand_data)

    if all_brand_data:
        try:
            with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
                json.dump(all_brand_data, f, indent=4, ensure_ascii=False)
            logging.info(f"SUCCESS: Scraping complete. Data saved to {OUTPUT_FILE}")
        except IOError as e:
            logging.error(f"FATAL: Could not write to output file {OUTPUT_FILE}. Reason: {e}")
    else:
        logging.warning("No data was scraped. The output file was not created.")

if __name__ == "__main__":
    main()