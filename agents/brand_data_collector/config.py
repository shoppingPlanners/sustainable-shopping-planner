# config.py

SUSTAINABILITY_KEYWORDS = [
    'sustainability', 'sustainable', 'eco-friendly', 'ethical', 'ethically',
    'environment', 'responsible', 'carbon footprint', 'recycled', 'organic',
    'conscious', 'supply chain', 'fair trade', 'eco', 'green'
]

SITE_CONFIGS = {
    # --- Universal Shopify Configuration (works for most sustainable brands) ---
    'shopify_default': {
        'product_link_selector': 'a[href*="/products/"], a.product-card__link, a.product-item__link, .product-grid-item a, .grid-product__link',
        'next_page_selector': 'a[rel="next"], .pagination__next, a.next',
        'product_name_selector': 'h1.product-title, h1[itemprop="name"], h1.product__title, .product-single__title, h1',
        'price_selector': 'span.price, span[itemprop="price"], .product__price, .product-price, .price-item',
        'category_selector': 'nav.breadcrumb a, .breadcrumbs a, nav a',
        'description_selector': 'div.product-description, div[itemprop="description"], .product__description, .product-single__description, p',
        'sizes_selector': 'select option, .variant-option, .size-option',
        'bestseller_badge_selector': '.badge, .product-badge, .label',
        'image_selector': 'img[itemprop="image"], .product__image img, .product-single__photo img, img',
    },
    
    # --- Everlane ---
    'everlane.com': {
        'product_link_selector': 'a[href*="/products/"], .ProductCard a, .product-card a',
        'next_page_selector': 'a.next, a[rel="next"]',
        'product_name_selector': 'h1, .product-title, .ProductName',
        'price_selector': '.price, .ProductPrice, span[data-testid="price"]',
        'category_selector': 'nav a, .breadcrumb a',
        'description_selector': '.product-description, .ProductDescription, p',
        'sizes_selector': '.size-option, button[data-size]',
        'bestseller_badge_selector': '.badge, .ProductBadge',
        'image_selector': 'img.ProductImage, img[alt*="product"]',
    },
    
    # --- Patagonia ---
    'patagonia.com': {
        'product_link_selector': 'a[href*="/product/"], a.product-tile, .product-card a',
        'next_page_selector': 'a.next-page, button[aria-label="Next"]',
        'product_name_selector': 'h1.product-title, h1',
        'price_selector': 'span.price, .product-price, [data-testid="price"]',
        'category_selector': 'nav.breadcrumbs a, nav a',
        'description_selector': 'div.product-description, .pdp-description',
        'sizes_selector': 'select#size option, button.size-button',
        'bestseller_badge_selector': 'span.badge, .bestseller',
        'image_selector': 'img.product-image',
    },

    # --- Reformation (Shopify) ---
    'thereformation.com': {
        'product_link_selector': 'a.product-card__link, a.ProductItem__Link',
        'next_page_selector': 'a[rel="next"], a.pagination__next',
        'product_name_selector': 'h1.product-title, h1.ProductMeta__Title',
        'price_selector': 'span.price, span.ProductMeta__Price',
        'category_selector': 'nav.breadcrumb a, .product-category',
        'description_selector': 'div.product-description, div.ProductMeta__Description',
        'sizes_selector': 'select.product-form__input option, fieldset.size-selector button',
        'bestseller_badge_selector': 'span.badge--sale, .product-badge',
        'image_selector': 'img.product-image, img.ProductImage',
    },

    # --- Pact (Shopify) ---
    'wearpact.com': {
        'product_link_selector': 'a.product-card__link, a.grid-product__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-single__title',
        'price_selector': 'span.product-single__price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.product-single__description',
        'sizes_selector': 'select[name="Size"] option, fieldset.size-selector button',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product-featured-image',
    },

    # --- Thought Clothing (Shopify) ---
    'thoughtclothing.com': {
        'product_link_selector': 'a.product-item__link, a.ProductItem__Link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product__title',
        'price_selector': 'span.product__price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product__description',
        'sizes_selector': 'select.product-form__input option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product__media',
    },

    # --- Organic Basics ---
    'organicbasics.com': {
        'product_link_selector': 'a.product-card, a.ProductCard',
        'next_page_selector': 'a[rel="next"], button.pagination-next',
        'product_name_selector': 'h1.product-title, h1.ProductTitle',
        'price_selector': 'span.product-price, .ProductPrice',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description, .ProductDescription',
        'sizes_selector': 'select.size-selector option, button.size-option',
        'bestseller_badge_selector': 'span.badge, .product-badge',
        'image_selector': 'img.product-image',
    },
    
    # --- Allbirds ---
    'allbirds.com': {
        'product_link_selector': 'a.product-tile, a[data-testid="product-link"]',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-name, h1[data-testid="product-name"]',
        'price_selector': 'span.price, div.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Nisolo ---
    'nisolo.com': {
        'product_link_selector': 'a.product-card, a.grid-product__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-single__title',
        'price_selector': 'span.product-single__price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.product-single__description',
        'sizes_selector': 'select.size-select option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product-featured-image',
    },

    # --- Rothy's ---
    'rothys.com': {
        'product_link_selector': 'a.ProductCard, a.product-card',
        'next_page_selector': 'a[aria-label="Next"]',
        'product_name_selector': 'h1.ProductTitle',
        'price_selector': 'span.ProductPrice',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.ProductDescription',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Vivobarefoot ---
    'vivobarefoot.com': {
        'product_link_selector': 'a.product-tile__link',
        'next_page_selector': 'a.pagination__next',
        'product_name_selector': 'h1.product__title',
        'price_selector': 'span.product__price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product__description',
        'sizes_selector': 'select.size-selector option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product__image',
    },

    # --- Kotn ---
    'kotn.com': {
        'product_link_selector': 'a.product-card, a.ProductItem__Link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product__title',
        'price_selector': 'span.product__price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product__description',
        'sizes_selector': 'select.product-form__input option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product__image',
    },

    # --- Mate the Label ---
    'matethelabel.com': {
        'product_link_selector': 'a.product-card, a.grid-product__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-single__title',
        'price_selector': 'span.product-single__price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.product-single__description',
        'sizes_selector': 'select[name="Size"] option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product-featured-image',
    },

    # --- Alternative Apparel ---
    'alternativeapparel.com': {
        'product_link_selector': 'a.product-item__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product__title',
        'price_selector': 'span.product__price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product__description',
        'sizes_selector': 'select.size-select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product__media',
    },

    # --- Armed Angels ---
    'armedangels.com': {
        'product_link_selector': 'a.product-tile',
        'next_page_selector': 'a.pagination-next',
        'product_name_selector': 'h1.product-name',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Girlfriend Collective ---
    'girlfriend.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Tentree ---
    'tentree.com': {
        'product_link_selector': 'a.product-card, a.grid-product__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-single__title',
        'price_selector': 'span.product-single__price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.product-single__description',
        'sizes_selector': 'select[name="Size"] option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product-featured-image',
    },

    # --- prAna ---
    'prana.com': {
        'product_link_selector': 'a.product-tile__link',
        'next_page_selector': 'a.pagination__next',
        'product_name_selector': 'h1.product__title',
        'price_selector': 'span.product__price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product__description',
        'sizes_selector': 'select.size-selector option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product__image',
    },

    # --- Organic Cotton Plus ---
    'organiccottonplus.com': {
        'product_link_selector': 'a.product-item',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-name',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Eileen Fisher ---
    'eileenfisher.com': {
        'product_link_selector': 'a.product-tile',
        'next_page_selector': 'a.next-page',
        'product_name_selector': 'h1.product-name',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Cuyana ---
    'cuyana.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- People Tree ---
    'peopletree.co.uk': {
        'product_link_selector': 'a.product-item__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product__title',
        'price_selector': 'span.product__price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product__description',
        'sizes_selector': 'select.product-form__input option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product__media',
    },

    # --- Outerknown ---
    'outerknown.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- ABLE ---
    'ableclothing.com': {
        'product_link_selector': 'a.product-card, a.grid-product__link',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-single__title',
        'price_selector': 'span.product-single__price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.product-single__description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.product-badge',
        'image_selector': 'img.product-featured-image',
    },

    # --- Matt & Nat ---
    'mattandnat.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-name',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Angela Roi ---
    'angelajoi.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Tradeland ---
    'tradelandco.com': {
        'product_link_selector': 'a.product-item',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-name',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- SERRV ---
    'serrv.org': {
        'product_link_selector': 'a.product-link',
        'next_page_selector': 'a.next',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Global Goods ---
    'globalgoods.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- AGOLDE ---
    'agolde.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.product-price',
        'category_selector': 'nav.breadcrumbs a',
        'description_selector': 'div.product-description',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Outland Denim ---
    'outlanddenim.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Wuxly ---
    'wuxly.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Veerah ---
    'veerah.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'button.size-button',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Tonlé ---
    'tonle.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },

    # --- Christy Martin Design ---
    'christymartindesign.com': {
        'product_link_selector': 'a.product-card',
        'next_page_selector': 'a[rel="next"]',
        'product_name_selector': 'h1.product-title',
        'price_selector': 'span.price',
        'category_selector': 'nav.breadcrumb a',
        'description_selector': 'div.description',
        'sizes_selector': 'select option',
        'bestseller_badge_selector': 'span.badge',
        'image_selector': 'img.product-image',
    },
}
