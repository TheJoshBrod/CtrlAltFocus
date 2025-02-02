import sys
import time
import yaml
import winreg
import random
import threading

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import incentive as pn
from inactivity_tracker import InactivityTracker
from main import snoopy_popup

# Time threshold for inactivity (in seconds)
INACTIVITY_THRESHOLD = 5  # Adjust as needed
last_active_time = time.time()  # Store the time of the last activity (mouse or keyboard event)

def get_default_browser(browser=""):
    try:
        # Open the registry key that contains the default browser
        registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                  r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
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
            # Setup the WebDriver with the EdgeDriverManager
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

def incentive(enabled_incentives: list, driver, tracker) -> None:
    print("Punishing!")
    if (len(enabled_incentives) == 0):
        print("No incentive selected")
        return

    incentive_pos = random.randint(0, len(enabled_incentives) - 1)
    incentive = enabled_incentives[incentive_pos]

    if (incentive == "Tab_Zapper"):
        print("Tab_Zapper")
        pn.tab_zapper(driver, tracker)
    elif (incentive == "Tab_Shuffler"):
        print("Tab_Shuffler")
        pn.tab_shuffler(driver)
    elif (incentive == "Pop_Up_Generator"):
        print("Pop_Up_Generator")
    elif (incentive == "Noise_Maker"):
        print("Noise_Maker")
        pn.noise_maker(driver, tracker)
    elif (incentive == "Constellation_Mode"):
        print("Constellation_Mode")
        pn.constellation_mode(driver,tracker)
    elif (incentive == "Brainrot_Mode"):
        print("Brainrot_Mode")
    elif(incentive == "Rick_Roll"):
        print("Rick_Roll")
        pn.rickroll(driver, tracker)
    else:
        print(f"Error: {incentive}")

def main() -> None:
    driver = get_default_browser()
    driver.get('https://google.com')

    # Load configuration
    with open("config_files.yaml", "r") as file:
        config = yaml.safe_load(file)

    incentive_options = config["Productivity_Incentives"]
    enabled_incentives = [key for key, value in incentive_options.items() if value]
    
    bop_it_mode = config["Productivity_Antidote"]["Bop_It_Enabled"]
    try:
        tracker = InactivityTracker(10, bop_it_mode)
        tracker_thread = threading.Thread(target=tracker.start_listening, daemon=True)
        tracker_thread.start()

        while True:
            if not tracker.is_active():
                snoopy_popup(driver, tracker)
                # Apply incentive if inactivity detected
                incentive(enabled_incentives, driver, tracker)    
            time.sleep(60)
        tracker_thread.join()
    except KeyboardInterrupt:
        tracker.stop_listening()
        sys.exit()
        tracker_thread.join()
    except Exception as e:
        tracker.stop_listening()
        sys.exit()
        tracker_thread.join()
        
if __name__ == "__main__":
    main()