# --- Data Parsing Logic ---
from typing import Dict, Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utilities import extract_asin_from_url, extract_brand, calculate_fba_score
from amazon_selectors import (
    TITLE_SELECTORS,
    URL_SELECTORS,
    PRICE_SELECTORS,
    RATING_SELECTORS,
    REVIEWS_SELECTORS,
    BADGE_SELECTORS
)

def find_element_with_selectors(element: WebElement, selectors: list, get_attr: str = None) -> str:
    """
    Try multiple selectors to find an element and extract text or attribute
    
    Args:
        element: Parent WebElement to search within
        selectors: List of CSS selectors to try
        get_attr: Attribute to extract instead of text (optional)
    
    Returns:
        Extracted text or attribute value, or empty string if not found
    """
    for selector in selectors:
        try:
            found = element.find_element(By.CSS_SELECTOR, selector)
            if get_attr:
                value = found.get_attribute(get_attr) or ""
            else:
                value = found.text.strip() or found.get_attribute("innerHTML") or ""
                
            if value:
                return value
        except NoSuchElementException:
            continue
    return ""

def extract_rank(element: WebElement, position: int = None) -> str:
    """Extract product rank from badge or use position"""
    # Try to extract badge text
    badge_text = find_element_with_selectors(element, BADGE_SELECTORS)
    
    # Check if badge has relevant text
    if badge_text and any(x in badge_text.lower() for x in ["#", "best", "seller", "top"]):
        return badge_text
        
    # Use position as fallback
    return f"#{position}" if position else "Unknown"

def extract_product_data(element: WebElement) -> Dict[str, str]:
    """Extract all data fields from product element"""
    data = {}
    
    # Extract basic fields
    data['title'] = find_element_with_selectors(element, TITLE_SELECTORS, "title") or \
                    find_element_with_selectors(element, TITLE_SELECTORS)
    
    url = find_element_with_selectors(element, URL_SELECTORS, "href")
    data['url'] = url if url and "amazon.com" in url else None
    
    data['asin'] = extract_asin_from_url(data['url']) or "Unknown"
    data['price'] = find_element_with_selectors(element, PRICE_SELECTORS) or "N/A"
    data['rating'] = find_element_with_selectors(element, RATING_SELECTORS) or "N/A"
    
    reviews_text = find_element_with_selectors(element, REVIEWS_SELECTORS)
    data['reviews_count'] = reviews_text if reviews_text else "N/A"
    
    data['brand'] = extract_brand(data['title'])
    
    return data

def parse_product_data(product_element: WebElement, rank_position: int = None) -> Optional[Dict[str, str]]:
    """
    Extracts relevant data from a single product element.
    Returns a dictionary of product data or None if extraction fails.
    """
    try:
        # Extract rank (using position as fallback)
        data = {'rank': extract_rank(product_element, rank_position)}
        
        # Extract all other product data
        product_data = extract_product_data(product_element)
        data.update(product_data)
        
        # Calculate FBA opportunity score
        data['fba_opportunity_score'] = calculate_fba_score(
            data['price'], data['rating'], data['reviews_count'], data['rank']
        )
        
        # Basic validation - title and URL are essential
        if not data.get('title') or not data.get('url'):
            print(f"Missing essential data for a product")
            return None
        
        print(f"Successfully parsed: {data.get('title')[:40]}... (Rank: {data['rank']})")
        return data

    except Exception as e:
        print(f"Warning: Parser error: {e}")
        return None