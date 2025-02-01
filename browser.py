import time
from pynput import mouse, keyboard
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import winreg

# Time threshold for inactivity (in seconds)
INACTIVITY_THRESHOLD = 3  # Adjust as needed
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


def on_move(x, y):
    global last_active_time
    last_active_time = time.time()


def on_click(x, y, button, pressed):
    global last_active_time
    last_active_time = time.time()


def on_press(key):
    global last_active_time
    last_active_time = time.time()


def check_inactivity():
    global last_active_time
    if time.time() - last_active_time > INACTIVITY_THRESHOLD:
        print("Inactivity detected!")
        return True
    return False


def main() -> None:
    # Initialize Selenium WebDriver
    driver = get_default_browser()
    if isinstance(driver, str):
        print(driver)  # Error in detecting browser
        return

    driver.get('https://google.com')

    # Set up listeners for mouse and keyboard events
    with mouse.Listener(on_move=on_move, on_click=on_click) as mouse_listener, \
            keyboard.Listener(on_press=on_press) as keyboard_listener:

        while True:
            # Check if the system is idle for more than the threshold time
            if check_inactivity():
                # Open or focus the browser when inactivity is detected
                driver.execute_script("window.open('https://bing.com', '_blank');") # You can add any action here

            time.sleep(1)  # Check for inactivity every second


if __name__ == "__main__":
    main()