"""
Defines CSS selectors for extracting data from Amazon product pages.
These selectors may need periodic updates as Amazon changes their HTML structure.
"""

# Title selector options
TITLE_SELECTORS = [
    "div.p13n-sc-truncate", 
    "div.p13n-sc-truncate-two-line",
    "a.a-link-normal span.a-size-medium",
    "a.a-link-normal span.a-size-base-plus",
    "div[class*='p13n-sc-truncate']", 
    "a.a-link-normal span",
    "div[class*='_cDEzb_p13n-sc-css-line-clamp']"
]

# Product URL selector options
URL_SELECTORS = [
    "a.a-link-normal", 
    "a[class*='a-link-normal']",
    "div a.a-link-normal",
    "a.a-size-base"
]

# Price selector options
PRICE_SELECTORS = [
    "span.p13n-sc-price", 
    "span[class*='p13n-sc-price']",
    "span.a-price span.a-offscreen",
    "span.a-color-price",
    "span[class*='a-price']",
    "span.a-size-base.a-color-price"
]

# Rating selector options
RATING_SELECTORS = [
    "i.a-icon-star span.a-icon-alt",
    "i.a-icon-star-small span.a-icon-alt",
    "div.a-icon-row span.a-icon-alt",
    "div.a-row span.a-icon-alt"
]

# Reviews selector options
REVIEWS_SELECTORS = [
    "div.a-icon-row a.a-link-normal span",
    "a.a-size-small.a-link-normal",
    "a[href*='customerReviews'] span",
    "div.a-row a[href*='#customerReviews']"
]

# Badge/rank selector options
BADGE_SELECTORS = [
    "span.zg-bdg-text", 
    "span.a-badge-text",
    "span.a-color-success"
]

# Strategies for finding product elements with different selectors
PRODUCT_ELEMENT_STRATEGIES = [
    {"method": "CSS_SELECTOR", "locator": "div.zg-grid-item"},  # Common bestseller grid
    {"method": "CSS_SELECTOR", "locator": "div.zg-item"},  # Alternative grid structure
    {"method": "CSS_SELECTOR", "locator": "li.zg-item-immersion"},  # Another grid structure
    {"method": "ID", "locator": "gridItemRoot"},  # Older bestseller grid items
    {"method": "CSS_SELECTOR", "locator": "div[data-component-type='s-search-result']"},  # Search results
    {"method": "CSS_SELECTOR", "locator": "div.a-carousel-card"}  # Carousel items
]

# Strategies for finding next page links
NEXT_PAGE_SELECTORS = [
    "li.a-last a",
    "a.a-link-normal.a-text-normal[href*='page=']", 
    "ul.a-pagination li.a-last a",
    "span.zg-pagination-page-selected + a",
    "a[aria-label='Next page']"
]