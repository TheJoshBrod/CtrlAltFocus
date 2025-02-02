import glob
import time
import random
import pygame
from playsound import playsound


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
            tab_zapper_clean_up(driver)
            return          

        for x in range(6):
            time.sleep(1)
            if tracker.is_active():
                tab_zapper_clean_up(driver)
                return       
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()

        if tracker.is_active():
            tab_zapper_clean_up(driver)
            return       
        driver.switch_to.window(driver.window_handles[-1])

    tab_zapper_clean_up(driver)


def noise_maker(driver, tracker):
    noises = glob.glob("resources/audio/*")

    pygame.mixer.init()

    while not tracker.is_active():
        sound_file1 = random.choice(noises)
        sound_file2 = random.choice(noises)

        sound1 = pygame.mixer.Sound(sound_file1)
        sound2 = pygame.mixer.Sound(sound_file2)

        channel1 = sound1.play()
        channel2 = sound2.play()

        while pygame.mixer.get_busy():
            if tracker.is_active():
                pygame.mixer.stop()
                return
            time.sleep(1)

    pygame.mixer.stop()

def brainrot(tracker):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while not tracker.is_active():

        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            pygame.draw.circle(screen, "red", player_pos, 40)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_pos.y -= 300 * dt
            if keys[pygame.K_s]:
                player_pos.y += 300 * dt
            if keys[pygame.K_a]:
                player_pos.x -= 300 * dt
            if keys[pygame.K_d]:
                player_pos.x += 300 * dt

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000

    pygame.quit()
def constellation_mode(driver,tracker):
    pygame.init()
    screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
    width, height = screen.get_size()


    image = pygame.image.load('resources/space.jpg')
    image = pygame.transform.scale(image, (width, height))


    font = pygame.font.SysFont('Comic Sans MS', 100)  
    text_color = ('white')
    text_surface = font.render("Stop Spacing Out", True, text_color)


    angle = 0


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if tracker.is_active():
                running = False
                break


        screen.blit(image, (0, 0))


        rotated_text = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_text.get_rect(center=(width / 2, height / 2))


        screen.blit(rotated_text, rotated_rect)


        pygame.display.update()


        angle += 1


        pygame.time.Clock().tick(65)
    pygame.quit()
