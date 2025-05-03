# --- Configuration ---
# URL for the Electronics Best Sellers page
# http://www.amazon.com/gp/bestsellers
# https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_nav_wireless_0
TARGET_URL = "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_0"

# Output file name - both CSV and Excel options
OUTPUT_CSV_FILE = "amazon_electronics_bestsellers.csv"
OUTPUT_EXCEL_FILE = "amazon_electronics_bestsellers.xlsx"

# Maximum wait time in seconds for elements to appear
WAIT_TIMEOUT = 15  # Increased for better reliability

# Number of pages to scrape (Amazon typically shows 50 items per page)
PAGES_TO_SCRAPE = 2  # Will get top 100 items (2 pages of 50)

# User agent to appear as a regular browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"

# Adding subgategories you might be interested in (for future use)
ELECTRONICS_SUBCATEGORIES = {
    "Accessories & Supplies": "electronics_accessories",
    "Camera & Photo": "camera_photo",
    "Car & Vehicle Electronics": "car_electronics",
    "Cell Phones & Accessories": "mobile_electronics",
    "Computers & Accessories": "computers",
    "GPS & Navigation": "gps",
    "Headphones": "headphones",
    "Home Audio": "audio_video",
    "Portable Audio & Video": "portable_audio_video",
    "Wearable Technology": "wearable_tech"
}

print("Configuration loaded from config.py")