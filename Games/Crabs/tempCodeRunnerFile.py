import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pygame
import random
from Games.Utility.utility import DeckManager
from Games.Crabs.CrabsOOP import CrapsGame  # Import your CrapsGame class



# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Craps Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Load card images
card_images = {}
image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Images')
for image_file in os.listdir(image_path):
    if image_file.endswith('.png'):
        card_name = image_file[:-4]
        try:
            card_images[card_name] = pygame.image.load(os.path.join(image_path, image_file))
        except pygame.error:
            print(f"Unable to load image: {image_file}")

# Button class for UI elements
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_text(self, new_text):
        self.text = new_text

# Create buttons for betting and game control
place_bet_button = Button(WIDTH // 2 - 200, HEIGHT - 150, 200, 50, "Place Bet", GREEN, WHITE)
next_round_button = Button(WIDTH // 2 + 20, HEIGHT - 150, 200, 50, "Next Round", GREEN, WHITE)
come_out_button = Button(WIDTH - 220, 10, 200, 50, "Come Out", RED, WHITE)

# Create point bet buttons for possible point values
point_bet_buttons = {}
point_values = [4, 5, 6, 8, 9, 10]
for i, value in enumerate(point_values):
    x = 50 + (i % 3) * 120
    y = HEIGHT - 300 + (i // 3) * 70
    point_bet_buttons[value] = Button(x, y, 100, 50, f"Bet {value}", BLUE, WHITE)

def draw_game(screen, game, message, cards=None, roll_value=None):
    """Draw the game state on the screen."""
    screen.fill(GREEN)  
    
    # Display bankroll and current bets
    bankroll_text = font.render(f"Bankroll: ${game.get_bankroll()}", True, WHITE)
    screen.blit(bankroll_text, (10, 10))

    bet_text = font.render(f"Current Bet: ${game.current_bet}", True, WHITE)
    screen.blit(bet_text,(10 ,50))

    point_bet_text = font.render(f"Point Bet: ${game.get_point_bet()}", True ,WHITE)
    screen.blit(point_bet_text,(10 ,90))

    state_text = font.render(f"Game State: {game.get_game_state()}", True ,WHITE)
    screen.blit(state_text,(10 ,130))

    if game.get_point():
        point_text = font.render(f"Point: {game.get_point()}", True ,WHITE)
        screen.blit(point_text,(10 ,170))

    if roll_value is not None:
        roll_text = font.render(f"Roll: {roll_value}", True ,WHITE)
        screen.blit(roll_text,(10 ,210))

    message_text = font.render(message ,True ,WHITE)
    screen.blit(message_text,(WIDTH //2 - message_text.get_width() //2 ,HEIGHT -200))

    # Draw cards if available
    if cards:
        card_width ,card_height =100 ,140
        for i ,card in enumerate(cards):
            if card in card_images:
                card_image=card_images[card]
                card_image=pygame.transform.scale(card_image,(card_width ,card_height))
                screen.blit(card_image,(WIDTH //2 -110 +i *120 ,HEIGHT //2 -100))
            else:
                pygame.draw.rect(screen ,WHITE,(WIDTH //2 -110 +i *120 ,HEIGHT //2 -100 ,card_width ,card_height))
                card_text=font.render(card ,True ,BLACK)
                screen.blit(card_text,(WIDTH //2 -100 +i *120 ,HEIGHT //2 -50))

    # Draw buttons for betting and game control
    place_bet_button.draw(screen)
    next_round_button.draw(screen)
    come_out_button.draw(screen)

    # Draw point bet buttons only when in "point" state
    if game.get_game_state() == "point":
        for button in point_bet_buttons.values():
            button.draw(screen)

def main():
    """Main game loop."""
    game = CrapsGame()
    clock = pygame.time.Clock()
    
    bet_input =""
    input_active=True 
    message ="Place your bet!"
    
    cards=None 
    roll_value=None 

    while True:
        screen.fill(GREEN) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle placing bets and controlling the game state
                if place_bet_button.is_clicked(event.pos) and input_active:
                    try:
                        bet=int(bet_input)
                        if game.place_bet(bet):
                            input_active=False 
                            result,cards ,roll_value=game.play_round()
                            message=result 
                        else:
                            message="Invalid bet amount."
                    except ValueError:
                        message="Please enter a valid number."
                    bet_input=""
                
                elif next_round_button.is_clicked(event.pos) and not input_active:
                    if game.get_game_state() == "come_out":
                        input_active=True 
                        message="Place your bet!"
                        cards=None 
                        roll_value=None 
                    else:
                        result,cards ,roll_value=game.play_round()
                        message=result
                
                elif come_out_button.is_clicked(event.pos):
                    game.set_game_state("come_out")
                    message="Come out roll"
                    input_active=True 
                    cards=None 
                    roll_value=None
                
                # Handle point bet buttons only in "point" state
                if game.get_game_state() == "point":
                    for value ,button in point_bet_buttons.items():
                        if button.is_clicked(event.pos):
                            if game.place_point_bet(10,value): # Fixed bet amount of $10
                                message=f"Point bet of $10 placed on {value}"
                            else:
                                message="Not enough funds for point bet."

            # Handle keyboard input for betting amounts
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    pass 
                elif event.key == pygame.K_BACKSPACE:
                    bet_input=bet_input[:-1]
                else:
                    bet_input += event.unicode

        # Update the Come Out button text based on game state
        come_out_button.update_text("Come Out" if game.get_game_state() == "come_out" else "Point")

        draw_game(screen ,game,message,cards ,roll_value)

        if input_active:
            bet_surface=font.render(bet_input ,True ,BLACK)
            pygame.draw.rect(screen ,WHITE,(WIDTH //2 -100 ,HEIGHT -250 ,200 ,40))
            screen.blit(bet_surface,(WIDTH //2 -95 ,HEIGHT -245))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
