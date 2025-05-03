"""
Amazon FBA Product Research Tool - Main Entry Point
"""
import os
import sys
import time
import argparse
from datetime import datetime

# Import from local modules
import config
from driver_setup import get_chrome_driver
from scraper import get_products_from_page
from data_saver import save_to_csv, save_to_excel, save_all_formats

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Amazon FBA Product Research Tool')
    parser.add_argument('--category', '-c', help='Category to analyze (default: electronics)', 
                        default='electronics')
    parser.add_argument('--pages', '-p', type=int, help=f'Number of pages to scrape (default: {config.PAGES_TO_SCRAPE})', 
                        default=config.PAGES_TO_SCRAPE)
    parser.add_argument('--output', '-o', help='Output format: csv, excel, or both (default: both)', 
                        default='both')
    return parser.parse_args()

def print_header():
    """Print welcome header"""
    print("=" * 80)
    print("AMAZON FBA PRODUCT RESEARCH TOOL")
    print("=" * 80)
    print(f"Starting analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def print_summary(products):
    """Print summary of the analysis results"""
    high_potential = sum(1 for p in products if p['fba_opportunity_score'] >= 75)
    medium_potential = sum(1 for p in products if 50 <= p['fba_opportunity_score'] < 75)
    low_potential = len(products) - high_potential - medium_potential
    
    print("\nQUICK ANALYSIS SUMMARY:")
    print(f"- Total products analyzed: {len(products)}")
    print(f"- High FBA potential products: {high_potential}")
    print(f"- Medium FBA potential products: {medium_potential}")
    print(f"- Low FBA potential products: {low_potential}")
    
    print("\nNext steps for your FBA research:")
    print("1. Review the Excel file's 'FBA Analysis' sheet for top opportunities")
    print("2. Research sourcing options for high-potential products")
    print("3. Check competition using tools like Jungle Scout or Helium 10")
    print("4. Calculate potential margins including FBA fees")

def main():
    """Main entry point for the Amazon FBA Product Research Tool."""
    args = parse_arguments()
    print_header()
    
    # Get Chrome WebDriver
    print("\nInitializing web browser...")
    driver = get_chrome_driver()
    
    try:
        start_time = time.time()
        
        # Scrape products
        print(f"\nStarting data collection from {args.pages} pages...")
        products = get_products_from_page(config.TARGET_URL, driver, args.pages)
        
        if not products:
            print("\nNo products were found to analyze.")
            return
        
        # Save the data
        print(f"\nCollected data for {len(products)} products. Saving results...")
        
        if args.output.lower() == 'csv':
            save_to_csv(products)
        elif args.output.lower() == 'excel':
            save_to_excel(products)
        else:
            save_all_formats(products)
        
        # Summary
        elapsed_time = time.time() - start_time
        print(f"\nFBA product research completed in {elapsed_time:.1f} seconds")
        print_summary(products)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        if 'products' in locals() and products:
            save_all_formats(products)
    except Exception as e:
        print(f"\nError in main process: {e}")
    finally:
        print("\nClosing browser...")
        driver.quit()
        print("\nAnalysis complete!")
        
if __name__ == "__main__":
    main()