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

# Set a background color (RGB format)
background_color = (255, 255, 255)  # White color

# Main game loop
running = True
while running:
    # Fill the screen with the background color
    screen.fill(background_color)
    
    # Event handling
    # for event in pygame:

