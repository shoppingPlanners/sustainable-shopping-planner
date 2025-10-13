"""
Agent 1: Brand Data Collector
Scrapes and collects sustainability data from brand websites
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Brand Data Collector Agent",
    description="Scrapes and collects sustainability data from brand websites",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BRAND_COLLECTOR_PORT = int(os.getenv("BRAND_COLLECTOR_PORT", "5001"))
DATA_FILE = "brand_data.json"

# Pydantic Models
class ScrapeRequest(BaseModel):
    url: str
    brand_name: Optional[str] = None

class BrandData(BaseModel):
    brand_name: str
    url: str
    products: List[Dict[str, Any]]
    sustainability_commitments: List[str]
    certifications: List[str]
    scraped_at: datetime

# In-memory storage
brand_database = {}


class BrandScraper:
    """Scrapes brand websites for product and sustainability data"""
    
    def __init__(self):
        self.http_client = None
        self.sustainability_keywords = [
            'sustainable', 'eco-friendly', 'organic', 'recycled', 'fair trade',
            'carbon neutral', 'biodegradable', 'ethical', 'green', 'renewable',
            'zero waste', 'vegan', 'cruelty-free', 'B-Corp', 'FSC certified'
        ]
    
    async def initialize(self):
        """Initialize the scraper"""
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        logger.info("Brand scraper initialized")
    
    async def shutdown(self):
        """Cleanup resources"""
        if self.http_client:
            await self.http_client.aclose()
    
    async def scrape_brand(self, url: str, brand_name: Optional[str] = None) -> Dict[str, Any]:
        """Scrape a brand website for products and sustainability data"""
        
        try:
            logger.info(f"Scraping brand website: {url}")
            
            # Fetch the page
            response = await self.http_client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract brand name if not provided
            if not brand_name:
                brand_name = self._extract_brand_name(soup, url)
            
            # Extract products
            products = self._extract_products(soup, url)
            
            # Extract sustainability commitments
            commitments = self._extract_sustainability_commitments(soup)
            
            # Extract certifications
            certifications = self._extract_certifications(soup)
            
            brand_data = {
                'brand_name': brand_name,
                'url': url,
                'products': products,
                'sustainability_commitments': commitments,
                'certifications': certifications,
                'scraped_at': datetime.utcnow().isoformat(),
                'product_count': len(products)
            }
            
            logger.info(f"Successfully scraped {brand_name}: {len(products)} products, {len(commitments)} commitments")
            
            return brand_data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            raise
    
    def _extract_brand_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract brand name from page"""
        
        # Try meta tags
        meta_title = soup.find('meta', property='og:site_name')
        if meta_title and meta_title.get('content'):
            return meta_title['content']
        
        # Try title tag
        title = soup.find('title')
        if title:
            return title.text.split('|')[0].strip()
        
        # Fallback to domain
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '').split('.')[0].title()
    
    def _extract_products(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Extract product information"""
        
        products = []
        
        # Common product selectors
        product_selectors = [
            {'container': 'div.product-item', 'name': '.product-name', 'price': '.product-price', 'url': 'a'},
            {'container': 'div.product-card', 'name': '.product-title', 'price': '.price', 'url': 'a'},
            {'container': 'article.product', 'name': 'h2', 'price': '.price', 'url': 'a'},
            {'container': '.product', 'name': '.product-name', 'price': '.price', 'url': 'a'}
        ]
        
        for selector_config in product_selectors:
            product_elements = soup.select(selector_config['container'])
            
            if product_elements:
                for element in product_elements[:20]:  # Limit to 20 products
                    try:
                        product = self._extract_product_details(element, selector_config, base_url)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.debug(f"Could not extract product: {e}")
                        continue
                
                if products:
                    break
        
        return products
    
    def _extract_product_details(
        self,
        element: BeautifulSoup,
        selector_config: Dict[str, str],
        base_url: str
    ) -> Optional[Dict[str, Any]]:
        """Extract details for a single product"""
        
        product = {
            'product_name': 'N/A',
            'product_url': '',
            'price': 'N/A',
            'category': 'N/A',
            'available_sizes': [],
            'sustainability_focus': []
        }
        
        # Extract name
        name_elem = element.select_one(selector_config['name'])
        if name_elem:
            product['product_name'] = name_elem.text.strip()
        
        # Extract URL
        url_elem = element.select_one(selector_config['url'])
        if url_elem and url_elem.get('href'):
            href = url_elem['href']
            if href.startswith('http'):
                product['product_url'] = href
            else:
                from urllib.parse import urljoin
                product['product_url'] = urljoin(base_url, href)
        
        # Extract price
        price_elem = element.select_one(selector_config['price'])
        if price_elem:
            product['price'] = price_elem.text.strip()
        
        # Check for sustainability indicators
        text_content = element.text.lower()
        for keyword in self.sustainability_keywords:
            if keyword in text_content:
                product['sustainability_focus'].append(keyword)
        
        return product if product['product_name'] != 'N/A' else None
    
    def _extract_sustainability_commitments(self, soup: BeautifulSoup) -> List[str]:
        """Extract sustainability commitments and statements"""
        
        commitments = []
        
        # Look for sustainability sections
        sustainability_sections = soup.find_all(
            ['div', 'section', 'article'],
            class_=lambda x: x and any(
                keyword in x.lower()
                for keyword in ['sustainab', 'eco', 'environment', 'responsibility', 'impact']
            )
        )
        
        for section in sustainability_sections:
            paragraphs = section.find_all('p')
            for p in paragraphs:
                text = p.text.strip()
                if len(text) > 30 and any(keyword in text.lower() for keyword in self.sustainability_keywords):
                    commitments.append(text)
        
        # Also check meta descriptions
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            content = meta_desc['content']
            if any(keyword in content.lower() for keyword in self.sustainability_keywords):
                commitments.append(content)
        
        return list(set(commitments))[:10]  # Unique, limit to 10
    
    def _extract_certifications(self, soup: BeautifulSoup) -> List[str]:
        """Extract sustainability certifications"""
        
        certifications = []
        
        cert_keywords = [
            'B-Corp', 'B Corporation', 'Fair Trade', 'Organic', 'GOTS',
            'Cradle to Cradle', 'Bluesign', 'OEKO-TEX', 'FSC', 'Rainforest Alliance',
            'Carbon Neutral', 'Climate Neutral', 'Leaping Bunny', '1% for the Planet'
        ]
        
        text_content = soup.text
        
        for cert in cert_keywords:
            if cert.lower() in text_content.lower():
                certifications.append(cert)
        
        # Look for certification images
        cert_images = soup.find_all('img', alt=lambda x: x and any(
            cert.lower() in x.lower() for cert in cert_keywords
        ))
        
        for img in cert_images:
            alt_text = img.get('alt', '')
            for cert in cert_keywords:
                if cert.lower() in alt_text.lower() and cert not in certifications:
                    certifications.append(cert)
        
        return list(set(certifications))


# Global scraper instance
scraper = BrandScraper()


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("🚀 Starting Brand Data Collector Agent...")
    await scraper.initialize()
    
    # Load existing data if available
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                for item in data:
                    brand_database[item['url']] = item
            logger.info(f"Loaded {len(brand_database)} brands from cache")
    except Exception as e:
        logger.warning(f"Could not load cached data: {e}")
    
    logger.info("✅ Brand Data Collector Agent started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Brand Data Collector Agent...")
    await scraper.shutdown()
    
    # Save data
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(list(brand_database.values()), f, indent=2)
        logger.info("Saved brand data to file")
    except Exception as e:
        logger.error(f"Could not save data: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "agent": "Brand Data Collector",
        "version": "1.0.0",
        "status": "operational",
        "brands_collected": len(brand_database),
        "endpoints": {
            "scrape": "POST /scrape",
            "brands": "GET /brands",
            "brand": "GET /brands/{brand_id}",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "brands_in_database": len(brand_database)
    }


@app.post("/scrape")
async def scrape_brand_endpoint(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks
):
    """Scrape a brand website"""
    
    try:
        logger.info(f"Received scrape request for: {request.url}")
        
        # Check if already scraped recently
        if request.url in brand_database:
            cached_data = brand_database[request.url]
            scraped_time = datetime.fromisoformat(cached_data['scraped_at'])
            if (datetime.utcnow() - scraped_time).total_seconds() < 3600:  # 1 hour cache
                logger.info(f"Returning cached data for {request.url}")
                return {
                    "status": "success",
                    "data": cached_data,
                    "cached": True
                }
        
        # Scrape the brand
        brand_data = await scraper.scrape_brand(request.url, request.brand_name)
        
        # Store in database
        brand_database[request.url] = brand_data
        
        # Notify Rating Calculator Agent in background
        background_tasks.add_task(notify_rating_calculator, brand_data)
        
        return {
            "status": "success",
            "data": brand_data,
            "cached": False
        }
        
    except Exception as e:
        logger.error(f"Error in scrape endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/brands")
async def get_all_brands():
    """Get all collected brand data"""
    return {
        "status": "success",
        "count": len(brand_database),
        "brands": list(brand_database.values())
    }


@app.get("/brands/{brand_id}")
async def get_brand(brand_id: str):
    """Get specific brand data"""
    
    # Try to find by URL or name
    for url, data in brand_database.items():
        if brand_id in url or brand_id.lower() in data['brand_name'].lower():
            return {
                "status": "success",
                "data": data
            }
    
    raise HTTPException(status_code=404, detail="Brand not found")


@app.post("/scrape/batch")
async def scrape_batch(urls: List[str], background_tasks: BackgroundTasks):
    """Scrape multiple brands"""
    
    results = []
    
    for url in urls[:10]:  # Limit to 10 at once
        try:
            brand_data = await scraper.scrape_brand(url)
            brand_database[url] = brand_data
            results.append({"url": url, "status": "success", "data": brand_data})
            
            # Notify Rating Calculator
            background_tasks.add_task(notify_rating_calculator, brand_data)
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            results.append({"url": url, "status": "error", "error": str(e)})
    
    return {
        "status": "success",
        "results": results,
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "error"])
    }


async def notify_rating_calculator(brand_data: Dict[str, Any]):
    """Notify the Rating Calculator Agent about new brand data"""
    
    try:
        rating_calculator_url = os.getenv("RATING_CALCULATOR_URL", "http://localhost:5002")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{rating_calculator_url}/calculate",
                json=brand_data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                logger.info(f"Notified Rating Calculator about {brand_data['brand_name']}")
            else:
                logger.warning(f"Rating Calculator returned status {response.status_code}")
                
    except Exception as e:
        logger.warning(f"Could not notify Rating Calculator: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=BRAND_COLLECTOR_PORT)

