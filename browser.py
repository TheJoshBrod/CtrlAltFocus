import time
import winreg
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager



def get_default_browser(browser=""):
    try:
        # Open the registry key that contains the default browser
        registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
        prog_id, _ = winreg.QueryValueEx(registry, "Progid")
        
        if browser != "":
            prog_id = browser 
        # Check if the prog_id contains Firefox
        if "firefox" in prog_id.lower():
            # Set up the Firefox driver
            options = webdriver.FirefoxOptions()
            return webdriver.Firefox(options=options)
        elif "chrome" in prog_id.lower():
            options = webdriver.ChromeOptions()
            return webdriver.Chrome(options=options)
        elif "edge" in prog_id.lower():
            options = webdriver.EdgeOptions()
            
            # Setup the WebDriver with the EdgeDriverManager
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
  
            return driver
        else:
            return "Unknown Browser"
    except Exception as e:
        return f"Error: {e}"



def main() -> None:
   
    driver = get_default_browser()
    driver.get('https://google.com')
    while True:
        continue


if __name__ == "__main__":
    main() 