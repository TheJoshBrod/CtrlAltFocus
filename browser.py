import time
import yaml
import winreg
import random
import threading

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import punishment as pn
from inactivity_tracker import InactivityTracker


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

def punishment(enable_pushiments: list, driver, tracker) -> None:
    print("Punishing!")
    if (len(enable_pushiments) == 0):
        print("No Punishment selected")
        return

    punishment_pos = random.randint(0, len(enable_pushiments) - 1)
    punishment = enable_pushiments[punishment_pos]

    if (punishment == "Tab_Zapper"):
        print("Tab_Zapper")
        pn.tab_zapper(driver, tracker)
    elif (punishment == "Tab_Shuffler"):
        print("Tab_Shuffler")
        pn.tab_shuffler(driver)
    elif (punishment == "Fake_Tab_Shuffler"):
        print("Fake_Tab_Shuffler")
    elif (punishment == "Pop_Up_Generator"):
        print("Pop_Up_Generator")
    elif (punishment == "Noise_Maker"):
        print("Noise_Maker")
    elif (punishment == "Constellation_Mode"):
        print("Constellation_Mode")
    elif (punishment == "Brainrot_Mode"):
        print("Brainrot_Mode")
    elif(punishment == "Rick_Roll"):
        print("Rick_Roll")
        pn.rickroll(driver, tracker)
    else:
        print(f"Error: {punishment}")

def main() -> None:
    driver = get_default_browser()
    driver.get('https://google.com')

    # Load configuration
    with open("config_files.yaml", "r") as file:
        config = yaml.safe_load(file)

    punishment_options = config["Productivity_Punishments"]
    enabled_punishments = [key for key, value in punishment_options.items() if value]

    try:
        # Initialize and start the inactivity tracker
        tracker = InactivityTracker(inactivity_threshold=10)
        tracker_thread = threading.Thread(target=tracker.start_listening)
        tracker_thread.start()

        while True:
            # Check if the system is idle for more than the threshold time
            if not tracker.is_active():
                # Apply punishment if inactivity detected
                punishment(enabled_punishments, driver, tracker)    
            time.sleep(60)  # Check for inactivity every 5 seconds

        tracker_thread.join()  # Ensure the tracker thread completes if needed
    except KeyboardInterrupt:
        tracker.stop_listening()  # Stop listeners and clean up
        tracker_thread.join()  # Ensure tracker thread finishes
    except Exception as e:
        tracker.stop_listening()  # Stop listeners and clean up
        tracker_thread.join()  # Ensure tracker thread finishes
if __name__ == "__main__":
    main()