import time
import random

def tab_shuffler(driver):
    tablist = driver.window_handles;
    tabtitles = []
    conlist = []
    indexlist = list(range(len(tablist)))
    for tab in tablist:
        driver.switch_to.window(tab)
        title = driver.execute_script("return document.title;")
        icon = driver.execute_script("""
        var icon = document.querySelector("link[rel*='icon']");
        return icon ? icon.href : '';""")
        conlist.append(icon)
        tabtitles.append(title)

    random.shuffle(indexlist)
    random.shuffle(indexlist)
    
    for i in range(len(tablist)):
        driver.switch_to.window(tablist[i])
        driver.execute_script(f"document.title = '{tabtitles[indexlist[i]]}';")
        driver.execute_script(f"""
        var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = '{conlist[indexlist[i]]}';
        document.getElementsByTagName('head')[0].appendChild(link);
        """)


def rickroll(driver, tracker):
    driver.execute_script("window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ)');")

def tab_zapper_clean_up(driver):
    # Loop through all open windows
    for handle in driver.window_handles[-5:]:
        driver.switch_to.window(handle)
        tab_title = driver.title  # Get the title of the current tab
        # Check if the title matches one of the desired titles (1 to 5)
        if tab_title in ['1', '2', '3', '4', '5']:  # Comparing the tab title to string values
            driver.close()
    driver.switch_to.window(driver.window_handles[-1])

def tab_zapper(driver, tracker):

    # Create a custom HTML string
    custom_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>$</title>
    </head>
    <style>
    html, body {
            height: 100%;
            margin: 0;
    }
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
            <p>$</p>
        </div>
    </body>
    </html>
    """


    while not tracker.is_active():
        for x in range(5):
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            current_html = custom_html.replace("$", str(x+1))
            driver.execute_script("document.write(arguments[0]);", current_html)

        if tracker.is_active():
            break        

        for x in range(6):
            time.sleep(1)
            if tracker.is_active():
                break       
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()

        if tracker.is_active():
            break        
        driver.switch_to.window(driver.window_handles[-1])


    tab_zapper_clean_up(driver)
