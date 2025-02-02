# v4.py
import requests
import time
from selenium import webdriver
import threading
from snoopy_animations import global_snoopy_queue, root
import random
import re
from gtts import gTTS
import os
import platform
import uuid
import psutil
import pygame
from functools import lru_cache
import tempfile

# API and WebDriver initialization
def snoopy_popup(driver, tracker):
    url = "http://localhost:11434/api/generate"

    def call_llama_api(prompt):
        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            insult = data.get("response")

            if insult:
                insult = re.sub(r'[{}]+', '', insult)
                insult = re.sub(r'[^\w\s]', '', insult)
                insult = insult.strip()
                insult = insult.lower()
                if insult and insult[0].isalpha():
                    insult = insult[0].upper() + insult[1:]
                return insult
            else:
                print("Llama API returned no response.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling Llama API: {e}")
            return None
        except (ValueError, KeyError) as e:
            print(f"Error processing API response: {e}")
            return None

    # Pygame initialization
    pygame.mixer.init()
    try:
        MAX_CHANNELS = pygame.mixer.get_num_channels()
    except pygame.error:
        MAX_CHANNELS = 8

    channels = []
    for i in range(min(MAX_CHANNELS, 10)):
        channels.append(pygame.mixer.Channel(i))

    def speak_text(text, speed, temp_dir):
        try:
            unique_filename = str(uuid.uuid4()) + ".mp3"
            filepath = os.path.join(temp_dir, unique_filename)
            speak = gTTS(text=text, lang='en-GB', slow=False)
            speak.save(filepath)

            sound = pygame.mixer.Sound(filepath)

            for channel in channels:
                if not channel.get_busy():
                    channel.play(sound)
                    break
            else:
                sound.play()

            def cleanup_after_delay(filename):
                time.sleep(2)
                os.remove(filename)

            cleanup_thread = threading.Thread(target=cleanup_after_delay, args=(filepath,))
            cleanup_thread.daemon = True
            cleanup_thread.start()

        except Exception as e:
            print(f"Error in gTTS or Pygame: {e}")

    def monitor_tabs(snoopy_animations_queue, stop_event):
        try:
            while not stop_event.is_set():  # Check stop_event *frequently*
                tabs = driver.window_handles
                tab_titles = []

                for tab in tabs:
                    driver.switch_to.window(tab)
                    tab_titles.append(driver.title)

                prompt = f"""
                Creatively insult me to get back to work or to stop getting distracted (make it cohesive sentences).
                Focus on these tab activities: {', '.join(tab_titles)}
                """

                insult = call_llama_api(prompt)

                if insult:
                    print("prompt: ", prompt)
                    print("insult: ", insult)

                    screen_width = root.winfo_screenwidth()
                    screen_height = root.winfo_screenheight()

                    available_width = screen_width
                    available_height = screen_height

                    x_offset = random.randint(-(available_width // 2) + 25, (available_width // 2) - 200)
                    y_offset = random.randint(-(available_height // 2) + 75, (available_height // 2) - 75)

                    scale_factor = random.uniform(0.5, 1.5)
                    text_speed = random.uniform(0.2, 0.4)

                    snoopy_animations_queue.put((insult, x_offset, y_offset, scale_factor, text_speed))

                    speak_thread = threading.Thread(target=speak_text, args=(insult, text_speed, temp_dir))
                    speak_thread.daemon = True
                    speak_thread.start()

                time.sleep(2)  # Adjust sleep time as needed

        except KeyboardInterrupt:
            print("\nStopping tab monitoring...")
        finally:
            print("monitor_tabs thread finished.")  # Confirmation

    def check_tracker(pause_event):  # Use a pause event
        while True:  # Keep checking indefinitely
            if tracker.is_active():
                print("Tracker is active! Pausing program.")
                pause_event.set()  # Pause the monitor thread
                while tracker.is_active():  # Stay in this while loop until tracker is no longer active
                    time.sleep(1)  # Check every second
                print("Tracker is no longer active. Resuming program.")
                pause_event.clear()  # Resume the monitor thread

            time.sleep(1)  # Check every second

    def monitor_tabs(snoopy_animations_queue, stop_event, pause_event):
        try:
            while not stop_event.is_set():
                if not pause_event.is_set():  # Only run if not paused
                    tabs = driver.window_handles
                    tab_titles = []

                    for tab in tabs:
                        driver.switch_to.window(tab)
                        tab_titles.append(driver.title)

                    prompt = f"""
                    Creatively insult me to get back to work or to stop getting distracted (make it cohesive sentences).
                    Focus on these tab activities: {', '.join(tab_titles)}
                    """

                    insult = call_llama_api(prompt)

                    if insult:
                        print("prompt: ", prompt)
                        print("insult: ", insult)

                        screen_width = root.winfo_screenwidth()
                        screen_height = root.winfo_screenheight()

                        available_width = screen_width
                        available_height = screen_height

                        x_offset = random.randint(-(available_width // 2) + 25, (available_width // 2) - 200)
                        y_offset = random.randint(-(available_height // 2) + 75, (available_height // 2) - 75)

                        scale_factor = random.uniform(0.5, 1.5)
                        text_speed = random.uniform(0.2, 0.4)

                        snoopy_animations_queue.put((insult, x_offset, y_offset, scale_factor, text_speed))

                        speak_thread = threading.Thread(target=speak_text, args=(insult, text_speed, temp_dir))
                        speak_thread.daemon = True
                        speak_thread.start()

                    time.sleep(2)  # Adjust sleep time as needed
                else:
                    time.sleep(1)  # Check if paused every second

        except KeyboardInterrupt:
            print("\nStopping tab monitoring...")
        finally:
            driver.quit()  # Ensure driver is closed in finally block
            print("monitor_tabs thread finished.")

    # Main program execution
    stop_event = threading.Event()
    pause_event = threading.Event()  # Create a pause event

    monitor_thread = threading.Thread(target=monitor_tabs, args=(global_snoopy_queue, stop_event, pause_event),
                                      daemon=True)  # Pass the pause event
    monitor_thread.start()

    tracker_thread = threading.Thread(target=check_tracker, args=(pause_event,), daemon=True)  # Pass the pause event
    tracker_thread.start()

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            while True:
                try:
                    root.mainloop()
                except KeyboardInterrupt:
                    print("Keyboard interrupt detected. Closing...")
                    break
    finally:
        stop_event.set()  # Signal threads to stop (important!)
        monitor_thread.join(timeout=10)
        tracker_thread.join(timeout=10)
        if monitor_thread.is_alive():
            print("Monitor thread did not exit gracefully. Consider force termination if necessary.")
        if tracker_thread.is_alive():
            print("Tracker thread did not exit gracefully. Consider force termination if necessary.")
        print("All threads terminated.")