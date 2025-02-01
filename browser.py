from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

import winreg

def get_default_browser():
    try:
        # Open the registry key that contains the default browser
        registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
        prog_id, _ = winreg.QueryValueEx(registry, "Progid")
        
        # Check if the prog_id contains Firefox
        if "firefox" in prog_id.lower():
            return "Mozilla Firefox"
        else:
            return "Unknown Browser"
    except Exception as e:
        return f"Error: {e}"

print(f"Default Browser: {get_default_browser()}")




# Set up the Firefox driver
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

# Open a website
driver.get('https://google.com')

# Wait for the page to load (optional)
time.sleep(3)

# Close the tab
driver.close()
