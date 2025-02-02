import sys
import time
import pygame
import random
import socket

WIDTH, HEIGHT = 600, 400


def bopit_socket_handler(conn, addr, instruct, instruct_id):
    
    msg = str(instruct_id) + "$" + instruct
    raw_msg = msg.encode('utf-8')
    conn.sendall(raw_msg)

    try:
        data = conn.recv(1024)
        
        rec_id = ""
        pos = 0
        cur_char = data[0].decode("utf-8")
        while cur_char != "$":
            rec_id += cur_char 
            pos += 1
            cur_char = data[pos].decode("utf-8")
        if int(rec_id) != instruct_id:
            return -1
        pos += 1
        val = int.from_bytes(data[pos], byteorder="big")
        return val
    except Exception as e:
        data = -1


def bopit_socket_generator():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.settimeout(1)

    server_socket.bind(('localhost', 65432))

    server_socket.listen(1)

    conn, addr = server_socket.accept()
    
    return conn, addr

def render_text(text, font):
    txt_surface = font.render(text, True, pygame.Color('black'))
    return txt_surface

def failure_screen(screen, clock):
    screen.fill((255,0,0))
    title_text = "Failure"
    font_title = pygame.font.Font(None, 48)
    title_surface = render_text(title_text, font_title)
    title_x = (WIDTH - title_surface.get_width()) // 2  # Center horizontally
    title_y = (HEIGHT - title_surface.get_height()) // 2
    screen.blit(title_surface, (title_x, title_y))
    pygame.display.flip()
    clock.tick(60)
    time.sleep(1)

def instruction_screen(screen, clock, inputs) -> str:
    # Set up fonts
    font = pygame.font.Font(None, 36)
    font_title = pygame.font.Font(None, 48)
    
    # Create input box for bop it instruction
    input_box = pygame.Rect(50, 150, 500, 50)

    # Set background to white
    screen.fill((255, 255, 255))

    # Create title object
    title_text = "Bop it"
    title_surface = render_text(title_text, font_title)
    title_x = (WIDTH - title_surface.get_width()) // 2
    title_y = input_box.y - title_surface.get_height() - 10 
    screen.blit(title_surface, (title_x, title_y))

    # Create instruction object
    instruction = inputs[random.randint(0, len(inputs) - 1)]
    if "shake-it" not in instruction:
        text = f"Press the {instruction} button!" 
    else:
        text = "Shake your Wiimote!"
    txt_surface = render_text(text, font)
    
    # Create logo object
    image_path = "resources/photos/controller.jpg"
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (100, 100))  # Resize image (optional)
    except pygame.error:
        print(f"Error loading image: {image_path}")
        sys.exit()

    # Draw instruction
    text_x = input_box.x + (input_box.width - txt_surface.get_width()) // 2
    text_y = input_box.y + (input_box.height - txt_surface.get_height()) // 2
    color = pygame.Color('lightskyblue3')
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(txt_surface, (text_x, text_y))
    
    # Draw the logo
    image_x = (WIDTH - image.get_width()) // 2
    image_y = input_box.y + input_box.height + 20
    screen.blit(image, (image_x, image_y))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

    return instruction

def game(inputs: list, speed: float, level: int) -> True:
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bop It!")

    # Main loop
    clock = pygame.time.Clock()
    last_update_time = pygame.time.get_ticks()

    conn, addr = bopit_socket_generator()


    # Instruction id
    instruct_id = 0

    # Escape condition
    messed_up = True
    while messed_up:
        messed_up = False

        for x in range(level):
            instruct_id += 1
            instruct = instruction_screen(screen, clock, inputs)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # TODO remove this code block
                
            time.sleep(1)
            
            current_time = time.time()
            last_update_time = current_time
            while current_time - last_update_time <= speed:
                current_time = time.time()
                
                socket_response = bopit_socket_handler(conn, addr, instruct, instruct_id)

                if socket_response == 0:
                    messed_up = True
                    break
                if socket_response == 1:
                    break
        
            if socket_response == 0:
                failure_screen(screen, clock)
                break

    conn.close()

def start(level: int) -> None:

    # Easy
    if level <= 2:
        speed = 10 - level
        inputs = ["A","B"]
    # Medium
    elif level <= 4:
        speed = 10 - level
        inputs = ["A","B","-","+","1","2"]
    # Hard
    elif level <= 9:
        inputs = ["A","B","-","+","1","2","shake-it"]
        speed = 10 - level
    # Impossible
    else:
        inputs = ["A","B","-","+","1","2","shake-it","left", "right", "up", "down"]
        speed = max(1 - 0.1 * (level - 9), 0.1) # Decrements at 0.1s, min val 0.1s  

    game(inputs, speed, level)

if __name__ == "__main__":
    # Test bop it
    start(1)