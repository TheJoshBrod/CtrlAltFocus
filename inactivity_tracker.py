import time
import threading
from pynput import mouse, keyboard

class InactivityTracker:
    def __init__(self, inactivity_threshold=4):
        self.inactivity_threshold = inactivity_threshold
        self.last_active_time = time.time()
        self.inactivity_event = threading.Event()
        
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        self.mutex = threading.Lock()
        self.end_condition_mutex = threading.Lock()


        self.stop_event = threading.Event() # End condition for listenr
        
    
    
    def on_move(self, x, y):
        with self.mutex:
            self.last_active_time = time.time()
            self.inactivity_event.set()  

    def on_click(self, x, y, button, pressed):
        with self.mutex:
            self.last_active_time = time.time()
            self.inactivity_event.set()

    def on_press(self, key):
        with self.mutex:
            self.last_active_time = time.time()
            self.inactivity_event.set()

    def check_inactivity(self):
        while True:
            with self.mutex:   
                if time.time() - self.last_active_time > self.inactivity_threshold:
                    self.inactivity_event.clear()
                    print("inactive")
                    
            time.sleep(1)

            with self.end_condition_mutex:
                if self.stop_event.is_set():
                    return

    def is_active(self):
        with self.mutex:
            return self.inactivity_event.is_set()

    def start_listening(self):
        # Start the listeners in separate threads
        self.mouse_thread = threading.Thread(target=self.mouse_listener.start)
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener.start)
        self.inactivity_thread = threading.Thread(target=self.check_inactivity)

        self.mouse_thread.start()
        self.keyboard_thread.start()
        self.inactivity_thread.start()

        self.mouse_thread.join()
        self.keyboard_thread.join()
        self.inactivity_thread.join()

    def stop_listening(self):    
        self.stop_event.set()
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.stop_event.set()

        self.mouse_thread.join()
        self.keyboard_thread.join()
        self.inactivity_thread.join()

        