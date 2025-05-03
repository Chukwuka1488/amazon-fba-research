"""
Browser configuration module to handle WebDriver setup across different operating systems.
"""
import os
import platform
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

def get_chrome_driver():
    """
    Creates and returns a Chrome WebDriver instance configured for the current operating system.
    Handles different OS-specific settings and common issues.
    """
    print(f"Setting up Chrome WebDriver for {platform.system()}...")
    
    # Set up Chrome options (common for all platforms)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # Uncomment the line below if you want headless mode (no browser UI)
    # chrome_options.add_argument("--headless")
    
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
            # macOS specific options if needed
            
        elif system == "windows":
            print("Detected Windows system")
            # Windows specific options if needed
            
        else:
            print(f"Warning: Unrecognized operating system: {system}")
        
        # Create the driver with managed WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
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