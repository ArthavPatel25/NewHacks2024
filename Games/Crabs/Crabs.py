import pygame
import sys
import random 

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crabs")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()
fps = 60

# Main game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state (put your game logic here)

    # Clear the screen
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw (add any drawing code here)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
