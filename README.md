# Amazon FBA Research Tool

A powerful scraping and analysis tool for Amazon FBA (Fulfillment By Amazon) product research. This tool helps sellers identify profitable products to sell on Amazon by analyzing top-selling products in various categories.

## Features

- **Web Scraping**: Extract product data from Amazon bestseller lists
- **FBA Opportunity Scoring**: Calculate opportunity scores based on price, rating, reviews and ranking
- **Detailed Analysis**: Export comprehensive product analysis to CSV and Excel files
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Anti-Detection Measures**: Implements techniques to avoid detection while scraping

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chukwuka1488/amazon-fba-research.git
cd amazon-fba-research
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to analyze Amazon bestsellers in the electronics category:

```bash
python main.py
```

### Command Line Options

- `--category` or `-c`: Category to analyze (default: electronics)
- `--pages` or `-p`: Number of pages to scrape (default: 2)
- `--output` or `-o`: Output format: csv, excel, or both (default: both)

Example:
```bash
python main.py --pages 3 --output excel
```

## Output

The tool generates two output files:

1. `amazon_electronics_bestsellers.csv`: A CSV file containing the raw scraped data
2. `amazon_electronics_bestsellers.xlsx`: An Excel file with multiple sheets including:
   - Products: All scraped product data
   - FBA Analysis: Products sorted by FBA opportunity score
   - Price Analysis: Distribution of products by price range
   - Summary: Overall metrics about the scraped data

## Project Structure

- `main.py`: Entry point for the application
- `config.py`: Configuration settings
- `browser.py`: WebDriver setup for different operating systems
- `scraper.py`: Logic for navigating Amazon and finding products
- `parser.py`: Extracts data from product elements
- `utilities.py`: Helper functions for data processing
- `data_saver.py`: Save and export functionality
- `analytics.py`: Analytics calculations
- `amazon_selectors.py`: CSS selectors for Amazon's HTML structure

## Disclaimer

This tool is for educational purposes only. Be sure to review Amazon's Terms of Service before scraping their website. Always use responsibly and ethically.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.