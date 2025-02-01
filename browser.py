import time
import yaml
import winreg
import random
from pynput import mouse, keyboard
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

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

def rickroll(driver):
    driver.execute_script("window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ)','_blank');")

def tab_zapper(driver):
    driver.execute_script("window.open('');")
    time.sleep(1)

    # Switch to the new tab (new tab is at index 1)
    driver.switch_to.window(driver.window_handles[1])

    # Create a custom HTML string
    custom_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>3</title>
    </head>
    <style>
    p {
        font-size: 100px;
    }
    div {
        align-items: center;
        display: flex;
        justify-content: center;
        height: 100%;
    }
    </style>
    <body>
        <div>
            <p>3</p>
        </div>
    </body>
    </html>
    """

    # Write the custom HTML content in the new tab
    driver.execute_script("document.write(arguments[0]);", custom_html)

def punishment(enable_pushiments: list, driver) -> None:
    if (len(enable_pushiments) == 0):
        print("No Punishment selected")
        return

    punishment_pos = random.randint(0, len(enable_pushiments) - 1)
    punishment = enable_pushiments[punishment_pos]

    if (punishment == "Tab_Zapper"):
        print("Tab_Zapper")
        tab_zapper(driver)
    elif (punishment == "Tab_Shuffler"):
        print("Tab_Shuffler")
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
    else:
        print(f"Error: {punishment}")


def main() -> None:
   
    driver = get_default_browser()

    driver.get('https://google.com')

    with open("config_files.yaml", "r") as file:
        config = yaml.safe_load(file)
    
    punishment_options = config["Productivity_Punishments"]
    enabled_punishments = [key for key, value in punishment_options.items() if value]
    
    # Set up listeners for mouse and keyboard events
    with mouse.Listener(on_move=on_move, on_click=on_click) as mouse_listener, \
            keyboard.Listener(on_press=on_press) as keyboard_listener:

        while True:
            # Check if the system is idle for more than the threshold time
            if check_inactivity():
                # Open or focus the browser when inactivity is detected
                punishment(enabled_punishments, driver)
                
            time.sleep(60)  # Check for inactivity every second


if __name__ == "__main__":
    main()