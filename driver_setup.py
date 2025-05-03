"""
Browser configuration module to handle WebDriver setup across different operating systems.
Optimized for Amazon scraping with anti-detection measures.
"""
import os
import platform
import sys
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import config

def get_chrome_driver():
    """
    Creates and returns a Chrome WebDriver instance configured for the current operating system.
    Includes optimizations specifically for Amazon scraping.
    """
    print(f"Setting up Chrome WebDriver for {platform.system()}...")
    
    # Set up Chrome options (common for all platforms)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Anti-detection measures
    chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Performance optimizations
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Uncomment for headless mode (no browser UI)
    # chrome_options.add_argument("--headless=new")  # new headless mode for newer Chrome versions
    
    # OS-specific configurations
    system = platform.system().lower()
    
    try:
        if system == "linux":
            print("Detected Linux system")
            # Additional Linux-specific options
            chrome_options.add_argument("--disable-extensions")
            
            # Ubuntu commonly needs this
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    if "ubuntu" in f.read().lower():
                        print("Ubuntu detected, applying specific settings")
                        # Add Ubuntu-specific options if needed
            
        elif system == "darwin":
            print("Detected macOS system")
            # macOS specific options
            chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            
        elif system == "windows":
            print("Detected Windows system")
            # Windows specific options
            chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            
        else:
            print(f"Warning: Unrecognized operating system: {system}")
        
        # Create the driver with managed WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Mask WebDriver presence
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set window size to a common resolution
        driver.set_window_size(1920, 1080)
        
        return driver
        
    except WebDriverException as e:
        print(f"Error setting up Chrome WebDriver: {e}")
        print("\nCommon solutions:")
        print("1. Make sure Google Chrome is installed")
        print("2. Check if your Chrome version is compatible with ChromeDriver")
        print("3. On Linux, you may need to install additional dependencies:")
        print("   Ubuntu/Debian: sudo apt install -y chromium-browser")
        print("   Fedora/RHEL: sudo dnf install -y chromium")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during driver setup: {e}")
        sys.exit(1)