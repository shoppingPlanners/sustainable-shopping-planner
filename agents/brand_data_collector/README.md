# Brand Data Collector Agent 🌿

An intelligent web scraping agent that collects product data from sustainable fashion brands.

## Features

- 🛍️ **Multi-Brand Support**: Configured for 6 major sustainable fashion brands
- 🔍 **Smart Scraping**: Automatically detects sustainability keywords in product descriptions
- 💾 **Database Integration**: Saves directly to MongoDB
- 📦 **JSON Export**: Creates `brand_data.json` for backup and portability
- 🎯 **Configurable Selectors**: Easy to add new brands via config.py

## Supported Brands

Currently configured to scrape **35+ sustainable fashion brands**:

### Major Sustainable Brands (6)
1. **Patagonia** - Outdoor clothing & gear with environmental focus
2. **Reformation** - Sustainable women's fashion
3. **Everlane** - Ethical basics & modern essentials
4. **Pact** - Organic cotton apparel
5. **Thought Clothing** - Natural & organic materials
6. **Organic Basics** - Sustainable essentials

### Footwear (4)
7. **Allbirds** - Wool & tree fiber shoes
8. **Nisolo** - Ethical leather footwear
9. **Rothy's** - Recycled plastic flats & sneakers
10. **Vivobarefoot** - Minimalist sustainable shoes

### Organic Basics & Essentials (4)
11. **Kotn** - Egyptian organic cotton
12. **Mate the Label** - Organic cotton basics
13. **Alternative Apparel** - Eco-friendly basics
14. **Armed Angels** - Fair trade fashion

### Activewear (4)
15. **Girlfriend Collective** - Recycled activewear
16. **Tentree** - Plant trees with purchases
17. **prAna** - Organic & recycled activewear
18. **Organic Cotton Plus** - Yoga & activewear

### Luxury & Designer (4)
19. **Eileen Fisher** - Timeless sustainable luxury
20. **Cuyana** - Fewer, better things
21. **People Tree** - Pioneer in sustainable fashion
22. **Outerknown** - Kelly Slater's eco brand

### Ethical Accessories (3)
23. **ABLE** - Empowering women globally
24. **Matt & Nat** - Vegan leather bags
25. **Angela Roi** - Luxury vegan handbags

### Fair Trade & Artisan (3)
26. **Tradeland** - Fair trade marketplace
27. **SERRV** - Handcrafted fair trade
28. **Global Goods** - Artisan products

### Eco-Friendly Denim (3)
29. **AGOLDE** - Sustainable denim
30. **Outland Denim** - Ethical jean production

### Sustainable Swimwear (2)
- Includes Patagonia & Outerknown collections

### Vegan Fashion (2)
31. **Wuxly** - Vegan outerwear
32. **Veerah** - Vegan luxury shoes

### Zero Waste & Circular (2)
33. **Tonlé** - Zero-waste Cambodian fashion
34. **Christy Martin Design** - Upcycled designs

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Websites

Edit `websites.txt` to add or modify brand URLs:

```
https://www.patagonia.com/shop/womens-clothing
https://www.thereformation.com/categories/clothing
...
```

### 3. Run the Collector

```bash
python run_collector.py
```

Or run directly:

```bash
python collector.py
```

### 4. View Results

Check the generated files:
- `brand_data.json` - All scraped product data
- MongoDB `brands` collection - Persisted in database

## How It Works

```
┌─────────────┐
│ websites.txt│──→ Read URLs
└─────────────┘
       ↓
┌─────────────┐
│  config.py  │──→ Get CSS selectors for each domain
└─────────────┘
       ↓
┌─────────────┐
│CategoryCrawl│──→ Navigate pages & extract product links
└─────────────┘
       ↓
┌─────────────┐
│Product Scrape──→ Extract: name, price, sizes, image, etc.
└─────────────┘
       ↓
┌─────────────────────┐
│Sustainability Check │──→ Detect eco-friendly keywords
└─────────────────────┘
       ↓
┌──────────────────┐
│Save to MongoDB   │
│& brand_data.json │
└──────────────────┘
```

## Configuration

### Adding a New Brand

1. Add the brand's URL to `websites.txt`

2. Add selectors to `config.py`:

```python
SITE_CONFIGS = {
    'newbrand.com': {
        'product_link_selector': 'a.product-link',
        'next_page_selector': 'a.next',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select.size option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },
}
```

### Sustainability Keywords

The agent automatically detects these keywords in product descriptions:

- sustainability, sustainable
- eco-friendly, ethical
- organic, recycled
- fair trade, carbon footprint
- conscious, supply chain
- green, responsible

Edit `SUSTAINABILITY_KEYWORDS` in `config.py` to customize.

## Data Structure

Each product contains:

```json
{
  "product_name": "Organic Cotton T-Shirt",
  "product_url": "https://brand.com/product/123",
  "price": "$45",
  "category": "Tops",
  "image": "https://brand.com/images/product.jpg",
  "available_sizes": ["S", "M", "L", "XL"],
  "is_bestseller": true,
  "sustainability_focus": ["organic", "fair trade"],
  "description": "Made from 100% organic cotton...",
  "rating": 4.5
}
```

## API Endpoint

The Flask app (run via `app.py`) provides:

- `GET /` - Health check
- `GET /brands` - List all scraped brands
- `GET /brands?limit=10` - Limit results

## Ethical Considerations

⚠️ **Important**: 

- Always respect `robots.txt`
- Follow each site's Terms of Service
- Rate limit your requests (built-in delays)
- Use for personal/educational purposes only
- Consider using official APIs when available

## Troubleshooting

### Issue: No products scraped

- **Solution**: CSS selectors may have changed. Inspect the website HTML and update `config.py`

### Issue: Connection timeout

- **Solution**: Some sites may block scrapers. Add delays or check your User-Agent header

### Issue: MongoDB connection error

- **Solution**: Ensure MongoDB is running and `DATABASE_URL` is set in `.env`

## Environment Variables

```env
DATABASE_URL=mongodb://localhost:27017/sustainable_shopping
```

## Development

To test a single brand:

```python
from scraper_agent import CategoryCrawler
from config import SITE_CONFIGS

crawler = CategoryCrawler(
    start_url="https://brand.com/category",
    config=SITE_CONFIGS['brand.com']
)
products = crawler.crawl()
print(f"Scraped {len(products)} products")
```

## License

This tool is for educational purposes. Please respect intellectual property and terms of service of scraped websites.

