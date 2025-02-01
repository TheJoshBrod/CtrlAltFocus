import time
import pynput
import winreg
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager


def get_default_browser(browser=""):
    try:
        # Open the registry key that contains the default browser
        registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
        prog_id, _ = winreg.QueryValueEx(registry, "Progid")
        
        if browser != "":
            prog_id = browser 
        # Check if the prog_id contains Firefox
        if "firefox" in prog_id.lower():
            options = webdriver.FirefoxOptions()
            return webdriver.Firefox(options=options)
        elif "chrome" in prog_id.lower():
            options = webdriver.ChromeOptions()
            return webdriver.Chrome(options=options)
        elif "edge" in prog_id.lower():
            options = webdriver.EdgeOptions()
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
            return driver
        elif "opera" in prog_id.lower():
            options = webdriver.ChromeOptions()
            options.binary_location = r"C:\Program Files\Opera GX\opera.exe"  # Path to Opera GX binary
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif "brave" in prog_id.lower():
            options = webdriver.ChromeOptions()
            options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Path to Brave binary
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        else:
            return "Unknown Browser"
    except Exception as e:
        return f"Error: {e}"



def main() -> None:
   
    driver = get_default_browser("brave")
    driver.get('https://google.com')

    mouse_last_moved = time.time()
    while True:
        continue


if __name__ == "__main__":
    main() 