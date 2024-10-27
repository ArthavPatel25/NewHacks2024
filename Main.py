import pygame
import sys
from Games.Roulette import Roulette
from Games.BlackJack import BlackJack
from Games.Crabs import Crabs

# Initialize pygame
pygame.init()

screen_info = pygame.display.Info()

# Screen width and height
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Screen")

# Load the background image
background_image = pygame.image.load("images/background.jpg")  # Replace with your image file path

# Resize the image to fit the screen (optional, if image size is different)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def create_button(text : str, pos : int):
    button_width = 200
    button_height = 25
    button_image = pygame.image.load("images/button.png")  # Replace with your button image file
    button_image = pygame.transform.scale(button_image, (button_width, button_height))  # Resize button to height and width
    button_x = (screen_width - button_width) // 2  # Center horizontally
    button_y = screen_height - button_height - pos   # pos pixels from the bottom
    button_rect = button_image.get_rect()
    button_rect.topleft = (button_x, button_y)
    # Define font for button text
    font = pygame.font.SysFont("Times New Roman", 25)  # Times New Roman with font size 25
    button_text = font.render(text, True, (255, 255, 255))  # White text
    text_rect = button_text.get_rect(center=button_rect.center)
    
    screen.blit(button_text, text_rect)

    return button_rect

# Main game loop
running = True
while running:
    # Fill the screen with a image
    screen.blit(background_image, (0, 0))
    quit_Button = create_button("Quit", 100)
    poker_Button = create_button("Poker", 150)
    blackjack_Button = create_button("Blackjack", 200)
    roulette_Button = create_button("Roulette", 250)
    craps_Button = create_button("Craps", 300)

    mouse_pos = pygame.mouse.get_pos()  # Get the x, y position of the mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop when the window is closed

        if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
            if quit_Button.collidepoint(mouse_pos):  # Check if button is clicked
                running = False
            elif roulette_Button.collidepoint(mouse_pos):
                Roulette.RouletteGame(100).runGame()
            elif blackjack_Button.collidepoint(mouse_pos):
                print("test")
                # BlackJack.Blackjack(100).runGame()
            elif craps_Button.collidepoint(mouse_pos):
                Crabs.main()
            elif poker_Button.collidepoint(mouse_pos):
                print("test")

    
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()



