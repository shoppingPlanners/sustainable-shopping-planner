# scraper_agent.py

import requests
import logging
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import SUSTAINABILITY_KEYWORDS

# Selenium imports for JavaScript-rendered sites
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium not available. Install with: pip install selenium webdriver-manager")

# Rating Calculator Agent URL
RATING_CALCULATOR_URL = "http://localhost:5002"

class CategoryCrawler:
    """Crawls a website category to scrape data for each product."""

    def __init__(self, start_url, config, brand_certifications=None):
        self.start_url = start_url
        self.config = config
        self.domain = urlparse(start_url).netloc
        self.scraped_products = []
        self.brand_certifications = brand_certifications or []
        self.session = requests.Session()
        # Improved headers to avoid bot detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })
        self.driver = None
        self.use_selenium = SELENIUM_AVAILABLE
        self.rating_calculator_available = self._check_rating_calculator()
    
    def _init_selenium_driver(self):
        """Initialize Selenium WebDriver for JavaScript-rendered sites"""
        if not SELENIUM_AVAILABLE:
            logging.warning("Selenium not available. Install with: pip install selenium webdriver-manager")
            self.use_selenium = False
            return
        
        if self.driver is not None:
            return
        
        try:
            logging.info("🌐 Initializing Selenium WebDriver...")
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            logging.info("✅ Selenium WebDriver initialized successfully")
        except Exception as e:
            logging.error(f"❌ Failed to initialize Selenium: {e}")
            logging.error(f"   Falling back to regular requests")
            self.use_selenium = False
    
    def _close_selenium_driver(self):
        """Close Selenium WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def _check_rating_calculator(self):
        """Check if Rating Calculator Agent is available"""
        try:
            response = requests.get(f"{RATING_CALCULATOR_URL}/health", timeout=2)
            if response.status_code == 200:
                logging.info(f"✅ Rating Calculator Agent available at {RATING_CALCULATOR_URL}")
                return True
        except:
            pass
        logging.warning(f"⚠️  Rating Calculator Agent not available - using fallback scoring")
        return False

    def _get_soup(self, url):
        """Fetches and parses a URL, returning a BeautifulSoup object or None on error."""
        # Add random delay to avoid being blocked (1-3 seconds)
        time.sleep(random.uniform(1.0, 3.0))
        
        # Force Selenium for known JavaScript-heavy e-commerce sites
        js_heavy_domains = ['everlane.com', 'patagonia.com', 'reformation.com', 'allbirds.com']
        if any(domain in url.lower() for domain in js_heavy_domains) and self.use_selenium:
            logging.info(f"  🌐 Using Selenium for JavaScript-heavy site")
            return self._get_soup_with_selenium(url)
        
        # Try regular requests first for other sites
        try:
            response = self.session.get(url, timeout=20, allow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if page has minimal content (likely JavaScript-rendered)
            if len(soup.get_text(strip=True)) < 500 and self.use_selenium:
                logging.info(f"  ⚡ Page appears JavaScript-rendered, trying Selenium...")
                return self._get_soup_with_selenium(url)
            
            return soup
            
        except requests.RequestException as e:
            logging.warning(f"  ⚠️  Regular fetch failed: {e}")
            
            # Try Selenium as fallback
            if self.use_selenium:
                logging.info(f"  ⚡ Trying Selenium for {url}")
                return self._get_soup_with_selenium(url)
            
            logging.error(f"Could not fetch {url}. Reason: {e}")
            return None
    
    def _get_soup_with_selenium(self, url):
        """Fetch page using Selenium for JavaScript-rendered content"""
        try:
            if self.driver is None:
                self._init_selenium_driver()
            
            if self.driver is None:
                return None
            
            logging.info(f"  🌐 Loading with Selenium: {url}")
            self.driver.get(url)
            
            # Wait for page to load - try multiple selectors
            wait = WebDriverWait(self.driver, 15)
            selectors_to_try = [
                (By.CSS_SELECTOR, 'a[href*="/products/"]'),  # Shopify product links
                (By.CLASS_NAME, 'product-card'),
                (By.CLASS_NAME, 'product-item'),
                (By.TAG_NAME, 'main'),
                (By.TAG_NAME, 'body')
            ]
            
            for selector_type, selector_value in selectors_to_try:
                try:
                    wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                    logging.info(f"  ✅ Page loaded (found: {selector_value})")
                    break
                except:
                    continue
            
            # Additional wait for JavaScript to finish rendering products (critical for e-commerce sites)
            time.sleep(15)
            
            # Scroll to load lazy-loaded content
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(1)
            except:
                pass
            
            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Log page content length
            text_length = len(soup.get_text(strip=True))
            logging.info(f"  📄 Page content: {text_length} characters")
            
            return soup
            
        except Exception as e:
            logging.error(f"  ❌ Selenium fetch failed for {url}: {e}")
            return None
    
    def _calculate_sustainability_score(self, product_data):
        """
        Call Rating Calculator Agent to get sustainability score.
        This is the proper agent-to-agent integration.
        """
        if not self.rating_calculator_available:
            return self._fallback_score(product_data)
        
        try:
            # Extract numeric price
            price = 0
            try:
                price_str = str(product_data.get('price', '0'))
                price = float(''.join(c for c in price_str if c.isdigit() or c == '.'))
            except:
                price = 0
            
            # Prepare data for Rating Calculator
            rating_request = {
                "product_name": product_data.get('product_name', ''),
                "category": product_data.get('category', ''),
                "price": price,
                "description": product_data.get('description', ''),
                "sustainability_focus": product_data.get('sustainability_focus', []),
                "certifications": self.brand_certifications
            }
            
            # Call Rating Calculator Agent API
            response = requests.post(
                f"{RATING_CALCULATOR_URL}/calculate_product_score",
                json=rating_request,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                logging.debug(f"  🎯 Rating Calculator scored: {result.get('sustainability_score')}/100")
                return {
                    'sustainability_score': result.get('sustainability_score', 50),
                    'rating': result.get('rating', 3.5),
                    'score_breakdown': result.get('score_breakdown', {}),
                    'scored_by': 'rating_calculator_agent'
                }
            else:
                logging.warning(f"  ⚠️  Rating Calculator returned {response.status_code}")
                return self._fallback_score(product_data)
                
        except Exception as e:
            logging.warning(f"  ⚠️  Rating Calculator error: {e}")
            return self._fallback_score(product_data)
    
    def _fallback_score(self, product_data):
        """Fallback scoring if Rating Calculator is unavailable"""
        score = 50
        
        # Add points for sustainability focus
        focus = product_data.get('sustainability_focus', [])
        score += len(focus) * 5
        
        # Add points for sustainability keywords in name
        name_lower = product_data.get('product_name', '').lower()
        if 'organic' in name_lower:
            score += 10
        if 'recycled' in name_lower:
            score += 10
        if 'sustainable' in name_lower or 'eco' in name_lower:
            score += 5
        
        score = min(100, max(40, score))
        rating = 3.0 + (score - 40) / 20
        
        return {
            'sustainability_score': int(score),
            'rating': round(rating, 1),
            'scored_by': 'fallback_heuristic'
        }

    def crawl(self, max_products=10):
        """Main crawling logic to navigate pages and orchestrate scraping."""
        current_url = self.start_url
        page_num = 1
        max_pages = 3  # Limit pages to avoid long scraping times
        
        while current_url and page_num <= max_pages:
            logging.info(f"Scraping category page {page_num}: {current_url}")
            soup = self._get_soup(current_url)
            if not soup:
                logging.warning(f"  ⚠️  Failed to fetch page {page_num}")
                break

            product_links = soup.select(self.config['product_link_selector'])
            logging.info(f"  📦 Found {len(product_links)} product links on page {page_num}")
            
            # Limit product links to process
            product_links = product_links[:min(len(product_links), max_products - len(self.scraped_products))]
            
            for i, link_tag in enumerate(product_links, 1):
                if len(self.scraped_products) >= max_products:
                    logging.info(f"  ✅ Reached maximum of {max_products} products")
                    break
                    
                product_url = urljoin(current_url, link_tag.get('href'))
                if not product_url or product_url == current_url:
                    continue
                    
                logging.info(f"  [{i}/{len(product_links)}] Scraping product...")
                product_data = self._scrape_product_page(product_url)
                if product_data:
                    self.scraped_products.append(product_data)
                    logging.info(f"  ✅ Product added (Total: {len(self.scraped_products)})")
                else:
                    logging.info(f"  ⚠️  Product skipped (no data)")
            
            # Check if we have enough products
            if len(self.scraped_products) >= max_products:
                logging.info(f"✅ Collected {len(self.scraped_products)} products for {self.domain}")
                break
            
            # Try to find next page
            next_page_tag = soup.select_one(self.config.get('next_page_selector'))
            if next_page_tag and next_page_tag.get('href'):
                current_url = urljoin(current_url, next_page_tag['href'])
                page_num += 1
            else:
                logging.info("  ℹ️  No more pages found")
                break
        
        # Cleanup Selenium driver if used
        self._close_selenium_driver()
        
        logging.info(f"🎉 Scraped {len(self.scraped_products)} products from {self.domain}")
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
            
            # Extract image
            image_url = ""
            image_selector = self.config.get('image_selector')
            if image_selector:
                img_tag = soup.select_one(image_selector)
                if img_tag:
                    image_url = img_tag.get('src') or img_tag.get('data-src') or ""
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin(url, image_url)
            
            # Scrape product data
            product_data = {
                "product_name": self._get_text(soup, self.config.get('product_name_selector')),
                "product_url": url,
                "price": self._get_text(soup, self.config.get('price_selector')),
                "category": self._get_text(soup, self.config.get('category_selector')),
                "image": image_url,
                "available_sizes": self._get_all_texts(soup, self.config.get('sizes_selector')),
                "is_bestseller": bool(soup.select_one(self.config.get('bestseller_badge_selector'))),
                "sustainability_focus": sustainability,
                "description": self._get_text(soup, self.config.get('description_selector'))[:200],  # First 200 chars
            }
            
            # 🎯 AGENT INTEGRATION: Call Rating Calculator to score this product
            score_data = self._calculate_sustainability_score(product_data)
            product_data['sustainability_score'] = score_data['sustainability_score']
            product_data['rating'] = score_data['rating']
            product_data['scored_by'] = score_data.get('scored_by', 'unknown')
            
            if 'score_breakdown' in score_data:
                product_data['score_breakdown'] = score_data['score_breakdown']
            
            logging.info(f"  ✅ Product scored: {score_data['sustainability_score']}/100 (by {score_data.get('scored_by', 'unknown')})")
            
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