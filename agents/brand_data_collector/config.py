# config.py

SUSTAINABILITY_KEYWORDS = [
    'sustainability', 'sustainable', 'eco-friendly', 'ethical', 'ethically',
    'environment', 'responsible', 'carbon footprint', 'recycled', 'organic',
    'conscious', 'supply chain', 'fair trade', 'eco', 'green'
]

SITE_CONFIGS = {
    # --- scrapeme.live ---
    'scrapeme.live': {
        'product_link_selector': 'li.product a.woocommerce-LoopProduct-link',
        'next_page_selector': 'a.next.page-numbers',
        'product_name_selector': 'h1.product_title',
        'price_selector': 'p.price .amount',
        'category_selector': 'span.posted_in a',
        'description_selector': 'div.woocommerce-product-details__short-description',
        'sizes_selector': None,
        'bestseller_badge_selector': 'span.onsale',
    },

    # --- automationexercise.com ---
    'automationexercise.com': {
        'product_link_selector': 'div.product-overlay a',
        'next_page_selector': 'ul.pagination li a[rel="next"]',
        'product_name_selector': 'div.product-information h2',
        'price_selector': 'div.product-information span span',
        'category_selector': 'div.choose ul li a',
        'description_selector': 'div.product-information p',
        'sizes_selector': None,
        'bestseller_badge_selector': None,
    },

    # --- automationpractice.pl ---
    'automationpractice.pl': {
        'product_link_selector': 'ul.product_list li.ajax_block_product a.product-name',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1',
        'price_selector': '#our_price_display',
        'category_selector': 'span.cat-name',
        'description_selector': '#short_description_content p',
        'sizes_selector': '#group_1 option',
        'bestseller_badge_selector': '.sale-label',
    },

    # --- webscraper.io test site ---
    'webscraper.io': {
        'product_link_selector': 'div.thumbnail a.title',
        'next_page_selector': 'ul.pagination li a[rel="next"]',
        'product_name_selector': 'h4.pull-right + h4',
        'price_selector': 'h4.pull-right.price',
        'category_selector': 'ul.breadcrumb li.active',
        'description_selector': 'p.description',
        'sizes_selector': None,
        'bestseller_badge_selector': None,
    },
}
