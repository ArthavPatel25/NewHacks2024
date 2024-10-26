import pygame
import sys
from Games.Crabs.Crabs import main as craps_main

# Initialize pygame
pygame.init()

screen_info = pygame.display.Info()

# Screen width and height
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Casino Games")

# Load the background image
background_image = pygame.image.load("images/background.jpg")  # Replace with your image file path
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def create_button(text: str, pos: int):
    button_color = (169, 169, 169)  # Grey color
    button_width = 200
    button_height = 25
    button_x = (screen_width - button_width) // 2  # Center horizontally
    button_y = screen_height - button_height - pos   # pos pixels from the bottom
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_border_radius = 20  # Radius for rounded corners

    # Define font for button text
    font = pygame.font.SysFont("Times New Roman", 25)  # Times New Roman with font size 25
    button_text = font.render(text, True, (255, 255, 255))  # White text

    pygame.draw.rect(screen, button_color, button_rect, border_radius=button_border_radius)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect

def launch_craps():
    craps_main()
    pygame.display.set_mode((screen_width, screen_height))  # Reset display to main menu size

def main_menu():
    running = True
    while running:
        # Fill the screen with the background image
        screen.blit(background_image, (0, 0))
        
        # Create buttons
        quit_button = create_button("Quit", 100)
        poker_button = create_button("Poker", 150)
        blackjack_button = create_button("Blackjack", 200)
        roulette_button = create_button("Roulette", 250)
        craps_button = create_button("Craps", 300)
        
        mouse_pos = pygame.mouse.get_pos()  # Get the x, y position of the mouse
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop when the window is closed

            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                if quit_button.collidepoint(mouse_pos):
                    running = False
                elif craps_button.collidepoint(mouse_pos):
                    launch_craps()
                # Add similar conditions for other game buttons when implemented
                # elif poker_button.collidepoint(mouse_pos):
