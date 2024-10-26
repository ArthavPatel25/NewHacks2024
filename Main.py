import pygame
import sys

# Initialize pygame
pygame.init()

screen_info = pygame.display.Info()

# Screen width and height
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Screen")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop when the window is closed
    
    # Fill the screen with a color (optional, just to show something on the screen)
    screen.fill((255, 255, 255))
    
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
