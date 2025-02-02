import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import queue
import time

root = tk.Tk()
root.withdraw()

def show_snoopy_animation(image_path1, image_path2, text, x_offset, y_offset, scale_factor, text_speed):
    # Snoopy Popup
    snoopy_popup = tk.Toplevel(root)
    snoopy_popup.overrideredirect(True)
    snoopy_popup.attributes('-topmost', True)
    snoopy_popup.attributes('-alpha', 0.0)  # Start transparent

    try:
        image1 = Image.open(image_path1).convert("RGBA")
        image2 = Image.open(image_path2).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Image file '{image_path1}' or '{image_path2}' not found.")
        return

    new_size = (int(200 * scale_factor), int(200 * scale_factor))
    image1 = image1.resize(new_size, Image.LANCZOS)
    image2 = image2.resize(new_size, Image.LANCZOS)

    photo1 = ImageTk.PhotoImage(image1)
    photo2 = ImageTk.PhotoImage(image2)

    label_image = tk.Label(snoopy_popup, image=photo1)
    label_image.image = photo1
    label_image.pack()

    image_state = 1

    def animate_snoopy():
        nonlocal image_state
        if image_state == 1:
            label_image.config(image=photo1)
            label_image.image = photo1
            image_state = 2
        else:
            label_image.config(image=photo2)
            label_image.image = photo2
            image_state = 1

        snoopy_popup.after(500, animate_snoopy)

    # Position Snoopy (relative to screen center, with offsets, accounting for image height)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_snoopy = (screen_width - new_size[0]) // 2 + x_offset

    # Key Change: Account for image height and vertical offset
    y_snoopy = (screen_height - new_size[1]) // 2 + y_offset - new_size[1] // 2 # Center vertically

    snoopy_popup.geometry(f"+{x_snoopy}+{y_snoopy}")

    # Make Snoopy clickable to disappear
    def on_snoopy_click(event):
        snoopy_popup.destroy()
        text_popup.destroy()

    label_image.bind("<Button-1>", on_snoopy_click)  # Bind left mouse click

    # Text Popup
    text_popup = tk.Toplevel(root)
    text_popup.overrideredirect(True)
    text_popup.attributes('-topmost', True)
    text_popup.attributes('-alpha', 0.0)  # Start transparent

    label_text = tk.Label(text_popup, text="", font=("Arial Bold", int(20 * scale_factor)), justify=tk.LEFT)
    label_text.pack()

    # Position Text (relative to Snoopy popup)
    x_text = x_snoopy + new_size[0] + 20
    y_text = y_snoopy
    text_popup.geometry(f"+{x_text}+{y_text}")

    max_text_width = screen_width - x_text - 20  # Use screen width for wrapping

    words = text.split()
    word_index_list = [0]
    current_text_list = [""]

    def show_text():
        def fade_in(alpha):
            if alpha <= 1.0:
                text_popup.attributes('-alpha', alpha)
                text_popup.update()
                text_popup.after(50, lambda: fade_in(alpha + 0.1))
            else:
                text_popup.attributes('-alpha', 1.0)

        if word_index_list[0] < len(words):
            current_text_list[0] += words[word_index_list[0]] + " "
            label_text.config(text=current_text_list[0])  # Set text first so we can get wraplength
            text_popup.update()  # Update to get correct wraplength

            available_width = max_text_width
            wraplength = min(screen_width, available_width)
            label_text.config(wraplength=wraplength)

            fade_in(0.1)
            word_index_list[0] += 1
            text_popup.after(int(text_speed * 1000), show_text)

    snoopy_popup.attributes('-alpha', 1.0)
    text_popup.attributes('-alpha', 1.0)

    animate_snoopy()
    show_text()


def process_queue(snoopy_animations_queue):
    try:
        item = snoopy_animations_queue.get_nowait()
        text, x_offset, y_offset, scale_factor, text_speed = item
        show_snoopy_animation("resources\photos\snoopy1.png", "resources\photos\snoopy2.png", text, x_offset, y_offset, scale_factor, text_speed)
    except queue.Empty:
        pass
    root.after(100, process_queue, snoopy_animations_queue)

# Initialize queue
snoopy_animations_queue = queue.Queue()
global_snoopy_queue = snoopy_animations_queue  # Make queue globally accessible

# Start queue processing in the main thread
root.after(0, process_queue, snoopy_animations_queue)

# Tkinter main loop will be started in main.py