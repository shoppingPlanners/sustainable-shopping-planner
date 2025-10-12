# config.py

"""
This is the BRAIN of the scraper.
Each website needs its own set of rules (selectors) because each website is built differently.
To find a selector: In Chrome, right-click the element -> "Inspect" -> right-click the HTML -> "Copy" -> "Copy selector".
"""

# Keywords to identify sustainability information in product descriptions
SUSTAINABILITY_KEYWORDS = [
    'sustainability', 'sustainable', 'eco-friendly', 'ethical', 'ethically',
    'environment', 'responsible', 'carbon footprint', 'recycled', 'organic',
    'conscious', 'supply chain', 'fair trade', 'eco', 'green'
]

# A dictionary where each key is a website's domain name
SITE_CONFIGS = {
    'scrapeme.live': {
        # === Rules for the main shop/category page ===
        'product_link_selector': 'li.product a.woocommerce-LoopProduct-link',
        'next_page_selector': 'a.next.page-numbers',

        # === Rules for the individual product page ===
        'product_name_selector': 'h1.product_title',
        'price_selector': 'p.price .amount',
        'category_selector': 'span.posted_in a',
        'description_selector': 'div.woocommerce-product-details__short-description',
        
        # This site does not have these details, so we set them to None
        'sizes_selector': None, 
        'bestseller_badge_selector': 'span.onsale', # This site uses an "On Sale" badge
    },

    # HOW TO ADD A NEW WEBSITE:
    # 'some_other_domain.com': {
    #     'product_link_selector': 'selector_for_product_links_on_this_site',
    #     'next_page_selector': 'selector_for_the_next_page_button',
    #     'product_name_selector': 'selector_for_product_name_on_detail_page',
    #     'price_selector': 'selector_for_price',
    #     'category_selector': 'selector_for_category',
    #     'description_selector': 'selector_for_the_product_description',
    #     'sizes_selector': 'selector_for_available_sizes',
    #     'bestseller_badge_selector': 'selector_for_a_bestseller_tag',
    # }
}