import sys
import pygame
import random

def game(inputs: list, speed: float) -> True:

    pygame.init()

    # Set up display
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Editable Text Window")

    # Set up fonts
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(50, 150, 500, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = 'Initial text'

    # Function to render text
    def render_text(text):
        txt_surface = font.render(text, True, pygame.Color('black'))
        return txt_surface

    # Main loop
    clock = pygame.time.Clock()
    while True:
        screen.fill((255, 255, 255))  # Fill the screen with white
        
        instruction = inputs[random.randint(0,len(inputs)-1)]
        if "shake-it" not in instruction:
            text = f"Press the {instruction} button!" 
        else:
            text = "Shake your Wiimote!"
        

        txt_surface = render_text(text)
        
        # Draw input box
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        
        # You can change the text programmatically here
        pygame.time.wait(1000)  # Wait for 1 second before changing the text
        # text = "Updated text!"  # Change the text programmatically after 1 second

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        # Update the display
        pygame.display.flip()
        clock.tick(30)

def start(inactivity_counter: int) -> None:

    # Easy
    if inactivity_counter <= 2:
        speed = 10 - inactivity_counter
        inputs = ["A","B"]
    # Medium
    elif inactivity_counter <= 4:
        speed = 10 - inactivity_counter
        inputs = ["A","B","-","+","1","2"]
    # Hard
    elif inactivity_counter <= 7:
        inputs = ["A","B","-","+","1","2","shake-it"]
        speed = 10 - inactivity_counter
    # Impossible
    else:
        inputs = ["A","B","-","+","1","2","shake-it","left", "right", "up", "down"]
        speed = max(10 - inactivity_counter, 1)

    game(inputs, speed)

if __name__ == "__main__":
    start(10)