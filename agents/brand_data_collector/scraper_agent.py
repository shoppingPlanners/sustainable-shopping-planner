# scraper_agent.py

import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import SUSTAINABILITY_KEYWORDS

class CategoryCrawler:
    """Crawls a website category to scrape data for each product."""

    def __init__(self, start_url, config):
        self.start_url = start_url
        self.config = config
        self.domain = urlparse(start_url).netloc
        self.scraped_products = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _get_soup(self, url):
        """Fetches and parses a URL, returning a BeautifulSoup object or None on error."""
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Could not fetch {url}. Reason: {e}")
            return None

    def crawl(self):
        """Main crawling logic to navigate pages and orchestrate scraping."""
        current_url = self.start_url
        page_num = 1
        while current_url:
            logging.info(f"Scraping category page {page_num}: {current_url}")
            soup = self._get_soup(current_url)
            if not soup:
                break

            product_links = soup.select(self.config['product_link_selector'])
            logging.info(f"Found {len(product_links)} product links on page {page_num}.")
            
            for link_tag in product_links:
                product_url = urljoin(current_url, link_tag.get('href'))
                product_data = self._scrape_product_page(product_url)
                if product_data:
                    self.scraped_products.append(product_data)
            
            next_page_tag = soup.select_one(self.config.get('next_page_selector'))
            if next_page_tag and next_page_tag.get('href'):
                current_url = urljoin(current_url, next_page_tag['href'])
                page_num += 1
            else:
                logging.info("No more pages found. Ending crawl for this category.")
                break
        
        return self.scraped_products

    def _scrape_product_page(self, url):
        """Scrapes all required details from a single product page."""
        logging.info(f"  -> Scraping product details from: {url}")
        soup = self._get_soup(url)
        if not soup:
            return None
        
        try:
            desc_text = self._get_text(soup, self.config.get('description_selector')).lower()
            sustainability = [kw for kw in SUSTAINABILITY_KEYWORDS if kw in desc_text]
            
            product_data = {
                "product_name": self._get_text(soup, self.config.get('product_name_selector')),
                "product_url": url,
                "price": self._get_text(soup, self.config.get('price_selector')),
                "category": self._get_text(soup, self.config.get('category_selector')),
                "available_sizes": self._get_all_texts(soup, self.config.get('sizes_selector')),
                "is_bestseller": bool(soup.select_one(self.config.get('bestseller_badge_selector'))),
                "sustainability_focus": sustainability,
            }
            return product_data
        except Exception as e:
            logging.error(f"Could not parse product page {url}. Reason: {e}")
            return None

    def _get_text(self, soup, selector):
        """Safely gets stripped text from a single element."""
        if not selector: return "N/A"
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "N/A"

    def _get_all_texts(self, soup, selector):
        """Safely gets a list of stripped texts from multiple elements."""
        if not selector: return []
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements] if elements else []