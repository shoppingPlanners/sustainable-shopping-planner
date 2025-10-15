# collector.py

import json
import logging
import os
from urllib.parse import urlparse
from scraper_agent import CategoryCrawler
from config import SITE_CONFIGS
from dotenv import load_dotenv
from pymongo import MongoClient

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(__file__)
WEBSITES_FILE = os.path.join(SCRIPT_DIR, "websites.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "brand_data.json")

# --- Setup Logging ---
# This provides detailed feedback in the terminal about what the script is doing.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_config_for_url(url):
    """Matches a URL to its specific configuration in config.py."""
    domain = urlparse(url).netloc.replace('www.', '')
    if domain in SITE_CONFIGS:
        return SITE_CONFIGS[domain]
    
    # Use universal Shopify config as fallback
    logging.info(f"No specific config for {domain}. Using universal Shopify selectors.")
    return SITE_CONFIGS.get('shopify_default')

def main():
    """Main function to run the data collection agent."""
    logging.info("Brand Data Collector Agent: Initializing...")
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    load_dotenv(os.path.join(ROOT_DIR, ".env"))
    load_dotenv()
    try:
        with open(WEBSITES_FILE, "r") as f:
            start_urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except FileNotFoundError:
        logging.error(f"FATAL: The file '{WEBSITES_FILE}' was not found. Please create it.")
        return

    if not start_urls:
        logging.error("FATAL: The 'websites.txt' file is empty. Please add category URLs to it.")
        return

    all_brand_data = []
    mongo_client = None
    db = None
    try:
        mongo_url = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/sustainable-shopping-planner')
        mongo_client = MongoClient(mongo_url)
        db = mongo_client.get_default_database()
        logging.info("Connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect MongoDB: {e}")
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

        # Persist each brand immediately to MongoDB
        if db is not None:
            try:
                db.brands.update_one(
                    {"brand_domain": brand_data["brand_domain"]},
                    {"$set": brand_data},
                    upsert=True
                )
                logging.info(f"Upserted brand {brand_data['brand_domain']} into MongoDB")
            except Exception as e:
                logging.error(f"Failed to upsert brand {brand_data['brand_domain']}: {e}")

    if all_brand_data:
        try:
            with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
                json.dump(all_brand_data, f, indent=4, ensure_ascii=False)
            logging.info(f"SUCCESS: Scraping complete. Data saved to {OUTPUT_FILE}")
        except IOError as e:
            logging.error(f"FATAL: Could not write to output file {OUTPUT_FILE}. Reason: {e}")
        # Also ensure data persisted in MongoDB
        if db is not None:
            try:
                db.meta.update_one({"_id": "brand_data"}, {"$set": {"product_count": sum(b.get("product_count", 0) for b in all_brand_data)}}, upsert=True)
            except Exception as e:
                logging.error(f"Failed to update meta in MongoDB: {e}")
    else:
        logging.warning("No data was scraped. The output file was not created.")

    if mongo_client:
        mongo_client.close()

if __name__ == "__main__":
    main()