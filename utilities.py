"""
Utility functions for Amazon scraper project.
"""
import re
from typing import Optional

def extract_numeric_price(price_text: str) -> Optional[float]:
    """Extract numeric value from price string like $15.99 or $1,234.56"""
    if price_text == "N/A" or not price_text:
        return None
    try:
        # Remove currency symbols and commas, then convert to float
        return float(re.sub(r'[^\d.]', '', price_text))
    except (ValueError, TypeError):
        return None

def extract_numeric_rating(rating_text: str) -> Optional[float]:
    """Extract numeric rating from text like '4.5 out of 5 stars'"""
    if rating_text == "N/A" or not rating_text:
        return None
    try:
        # Try to find a float value in the text
        rating_match = re.search(r'(\d+(\.\d+)?)', rating_text)
        if rating_match:
            return float(rating_match.group(1))
        return None
    except (ValueError, TypeError):
        return None

def extract_numeric_reviews(reviews_text: str) -> Optional[int]:
    """Extract number of reviews from text like '1,234 reviews'"""
    if reviews_text == "N/A" or not reviews_text:
        return None
    try:
        # Extract digits, removing commas and other characters
        return int(re.sub(r'[^\d]', '', reviews_text))
    except (ValueError, TypeError):
        return None

def extract_asin_from_url(url: str) -> Optional[str]:
    """Extract ASIN from Amazon product URL"""
    if not url or "amazon.com" not in url:
        return None
    try:
        # Look for ASIN pattern in URL
        asin_match = re.search(r'/dp/([A-Z0-9]{10})(?:/|\?|$)', url)
        if asin_match:
            return asin_match.group(1)
        return None
    except (ValueError, TypeError):
        return None

def extract_rank_number(rank_text: str) -> Optional[int]:
    """Extract numeric rank from text like '#5' or 'Best Seller #12'"""
    if rank_text == "Unknown" or not rank_text:
        return None
    try:
        # Look for numbers after # symbol
        rank_match = re.search(r'#(\d+)', rank_text)
        if rank_match:
            return int(rank_match.group(1))
        return None
    except (ValueError, TypeError):
        return None

def extract_brand(title: str) -> str:
    """Extract potential brand name from product title"""
    if not title:
        return "N/A"
    try:
        # Brand is often in the title before a hyphen or colon
        brand_match = re.match(r'^(.*?)[\s]*(-|:|–)[\s]*', title)
        if brand_match:
            potential_brand = brand_match.group(1).strip()
            # Most brand names are 1-3 words
            if len(potential_brand.split()) <= 3:
                return potential_brand
    except Exception:
        pass
    return "N/A"

def calculate_fba_score(price: str, rating: str, reviews: str, rank: str) -> int:
    """Calculate FBA opportunity score based on key metrics"""
    # Calculate price factor (max 25 points)
    price_points = calculate_price_factor(price)
    
    # Calculate rating factor (max 25 points)
    rating_points = calculate_rating_factor(rating)
    
    # Calculate review count factor (max 25 points)
    review_points = calculate_review_factor(reviews)
    
    # Calculate rank factor (max 25 points)
    rank_points = calculate_rank_factor(rank)
    
    return price_points + rating_points + review_points + rank_points

# Split calculation functions to keep file under 100 lines
def calculate_price_factor(price: str) -> int:
    price_value = extract_numeric_price(price)
    if not price_value:
        return 0
    
    if 15 <= price_value <= 50:
        return 25
    elif 10 <= price_value <= 75:
        return 15
    return 0

def calculate_rating_factor(rating: str) -> int:
    rating_value = extract_numeric_rating(rating)
    if not rating_value:
        return 0
    
    return min(25, int(rating_value * 5))

def calculate_review_factor(reviews: str) -> int:
    reviews_value = extract_numeric_reviews(reviews)
    if not reviews_value:
        return 0
    
    if 50 <= reviews_value <= 500:
        return 25
    elif 10 <= reviews_value <= 1000:
        return 15
    return 0

def calculate_rank_factor(rank: str) -> int:
    rank_value = extract_rank_number(rank)
    if not rank_value:
        return 0
    
    if rank_value <= 20:
        return 15  # Very competitive
    elif 21 <= rank_value <= 100:
        return 25  # Good balance
    elif 101 <= rank_value <= 500:
        return 20  # Less competitive but still popular
    return 0