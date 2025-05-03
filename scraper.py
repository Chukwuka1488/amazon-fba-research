# --- Page Scraping Logic ---
from typing import List, Dict
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
from parser import parse_product_data
from amazon_selectors import PRODUCT_ELEMENT_STRATEGIES, NEXT_PAGE_SELECTORS

def random_delay(min_seconds=1.0, max_seconds=3.0):
    """Add a random delay to appear more human-like"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def save_debug_html(driver, filename):
    """Save page source for debugging"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Saved page source to {filename} for debugging")
    except Exception as e:
        print(f"Failed to save page source: {e}")

def find_product_elements(driver):
    """Find product elements using multiple strategies"""
    for strategy in PRODUCT_ELEMENT_STRATEGIES:
        try:
            method = getattr(By, strategy["method"])
            locator = (method, strategy["locator"])
            print(f"Trying to find products using: {strategy['locator']}")
            
            # Wait for the products to be present
            WebDriverWait(driver, config.WAIT_TIMEOUT).until(
                EC.presence_of_element_located(locator)
            )
            
            # Get all matching elements
            elements = driver.find_elements(method, strategy["locator"])
            
            if elements:
                print(f"Found {len(elements)} product elements using {strategy['locator']}")
                return elements
        except Exception as e:
            print(f"Strategy {strategy['locator']} failed: {e}")
            continue
    
    return []

def go_to_next_page(driver):
    """Navigate to the next page of results"""
    # Try standard CSS selectors first
    for selector in NEXT_PAGE_SELECTORS:
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"Found next page link: {next_page.get_attribute('href')}")
            next_page.click()
            return True
        except NoSuchElementException:
            continue
    
    # Try to find links containing "Next page" text as fallback
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            if "next page" in link.text.lower():
                print(f"Found 'Next page' link: {link.text}")
                link.click()
                return True
    except Exception as e:
        print(f"Error finding next page by text: {e}")
    
    return False

def extract_products(product_elements, current_page):
    """Extract data from a list of product elements"""
    products = []
    for index, element in enumerate(product_elements):
        try:
            # Calculate rank position based on page and item index
            rank_position = (current_page - 1) * 50 + (index + 1)
            product_data = parse_product_data(element, rank_position)
            
            if product_data:
                product_data['page_found'] = current_page
                products.append(product_data)
                
        except Exception as e:
            print(f"Error parsing product {index + 1}: {e}")
    
    return products

def get_products_from_page(url, driver, pages_to_scrape=1):
    """Get product data from Amazon bestseller pages"""
    print(f"Navigating to: {url}")
    driver.get(url)
    random_delay(2.0, 4.0)
    
    all_products = []
    current_page = 1
    
    while current_page <= pages_to_scrape:
        print(f"\n--- Processing Page {current_page} of {pages_to_scrape} ---")
        
        # Find product elements
        product_elements = find_product_elements(driver)
        if not product_elements:
            print("No product elements found.")
            save_debug_html(driver, f"amazon_page_{current_page}_source.html")
            break
            
        # Extract product data
        page_products = extract_products(product_elements, current_page)
        all_products.extend(page_products)
        print(f"Extracted {len(page_products)} products from page {current_page}")
        
        # Go to next page if needed
        if current_page < pages_to_scrape:
            if not go_to_next_page(driver):
                print("Could not navigate to next page. Ending scraping.")
                break
            random_delay(2.0, 4.0)
            current_page += 1
        else:
            break
    
    print(f"Total products collected: {len(all_products)}")
    return all_products