import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pygame
import random
from Games.Utility.utility import DeckManager
from Games.Crabs.CrabsOOP import CrapsGame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Craps Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)

card_images = {}
image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Images')
background_image = pygame.image.load(os.path.join(image_path, 'pokerBackground.jpg'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

for image_file in os.listdir(image_path):
    if image_file.endswith('.png'):
        card_name = image_file[:-4]
        try:
            card_images[card_name] = pygame.image.load(os.path.join(image_path, image_file))
        except pygame.error:
            print(f"Unable to load image: {image_file}")

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

place_bet_button = Button(WIDTH // 2 - 200, HEIGHT - 150, 200, 50, "Place Bet", GREEN, WHITE)
next_round_button = Button(WIDTH // 2 + 20, HEIGHT - 150, 200, 50, "Next Round", GREEN, WHITE)
come_out_button = Button(WIDTH // 2 - 100, HEIGHT // 4, 200, 50, "Come Out", RED, WHITE)
return_to_menu_button = Button(WIDTH - 220, 10, 200, 50, "Return to Menu", RED, WHITE)

# point_bet_buttons = {}
# point_values = [4, 5, 6, 8, 9, 10]
# button_width, button_height = 100, 50
# button_spacing = 20
# total_button_width = (button_width * len(point_values)) + (button_spacing * (len(point_values) - 1))
# start_x = (WIDTH - total_button_width) // 2
# for i, value in enumerate(point_values):
#     x = start_x + i * (button_width + button_spacing)
#     y = HEIGHT * 3 // 4
#     point_bet_buttons[value] = Button(x, y, button_width, button_height, f"Bet {value}", BLUE, WHITE)
point_bet_buttons = {}
point_values = [4, 5, 6, 8, 9, 10]
button_width, button_height = 100, 50
button_spacing = 20
total_button_height = (button_height * len(point_values)) + (button_spacing * (len(point_values) - 1))
start_y = (HEIGHT - total_button_height) // 2
x = WIDTH // 4  # Halfway between the left edge and the center
for i, value in enumerate(point_values):
    y = start_y + i * (button_height + button_spacing)
    point_bet_buttons[value] = Button(x, y, button_width, button_height, f"Bet {value}", BLUE, WHITE)
def draw_game(screen, game, message, cards=None, roll_value=None, earnings=None):
    screen.blit(background_image, (0, 0))

    bankroll_text = font.render(f"Bankroll: ${game.get_bankroll()}", True, WHITE)
    screen.blit(bankroll_text, (10, 10))

    bet_text = font.render(f"Current Bet: ${game.current_bet}", True, WHITE)
    screen.blit(bet_text, (10, 50))

    point_bets = game.get_point_bets()
    y_offset = 90
    if point_bets:
        point_bets_text = font.render("Point Bets:", True, WHITE)
        screen.blit(point_bets_text, (10, y_offset))
        y_offset += 40
        for point, bet in point_bets.items():
            point_bet_text = font.render(f"  Bet on {point}: ${bet}", True, WHITE)
            screen.blit(point_bet_text, (10, y_offset))
            y_offset += 40
    else:
        no_point_bets_text = font.render("No Point Bets", True, WHITE)
        screen.blit(no_point_bets_text, (10, y_offset))
        y_offset += 40

    state_text = font.render(f"Game State: {'Come Out' if game.get_game_state() == 'come_out' else 'Point'}", True, WHITE)
    screen.blit(state_text, (10, y_offset))
    y_offset += 40

    if game.get_point():
        point_text = font.render(f"Point: {game.get_point()}", True, WHITE)
        screen.blit(point_text, (10, y_offset))
        y_offset += 40

    if roll_value is not None:
        roll_text = font.render(f"Roll: {roll_value}", True, WHITE)
        screen.blit(roll_text, (10, y_offset))
        y_offset += 40

    if earnings is not None:
        earnings_color = GREEN if earnings >= 0 else RED
        earnings_text = font.render(f"{'Earnings' if earnings >= 0 else 'Loss'}: ${abs(earnings)}", True, earnings_color)
        screen.blit(earnings_text, (10, y_offset))

    message_text = font.render(message, True, WHITE)
    screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT - 200))

    if cards:
        card_width, card_height = 150, 210
        card_spacing = 20
        total_width = (card_width * len(cards)) + (card_spacing * (len(cards) - 1))
        start_x = (WIDTH - total_width) // 2
        for i, card in enumerate(cards):
            if card in card_images:
                card_image = card_images[card]
                card_image = pygame.transform.scale(card_image, (card_width, card_height))
                screen.blit(card_image, (start_x + i * (card_width + card_spacing), HEIGHT // 2 - card_height // 2))
            else:
                pygame.draw.rect(screen, WHITE,
                                 (start_x + i * (card_width + card_spacing), HEIGHT // 2 - card_height // 2, card_width, card_height))
                card_text = font.render(card, True, BLACK)
                screen.blit(card_text, (start_x + i * (card_width + card_spacing) + 10, HEIGHT // 2))

    place_bet_button.draw(screen)
    next_round_button.draw(screen)
    come_out_button.draw(screen)
    return_to_menu_button.draw(screen)

    if game.get_game_state() == "point":
        for button in point_bet_buttons.values():
            button.draw(screen)

def main():
    game = CrapsGame()
    clock = pygame.time.Clock()

    bet_input = ""
    point_bet_input = ""
    input_active = True
    point_bet_active = False
    current_point_bet_value = None
    message = "Place your bet!"

    cards = None
    roll_value = None
    earnings = None
    previous_bankroll = game.get_bankroll()

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_menu_button.is_clicked(event.pos):
                    running = False

                elif place_bet_button.is_clicked(event.pos) and input_active:
                    try:
                        bet = int(bet_input)
                        if game.place_bet(bet):
                            input_active = False
                            result, cards, roll_value = game.play_round()
                            message = result
                            earnings = game.get_bankroll() - previous_bankroll
                            previous_bankroll = game.get_bankroll()
                        else:
                            message = "Invalid bet amount."
                    except ValueError:
                        message = "Please enter a valid number."
                    bet_input = ""

                elif next_round_button.is_clicked(event.pos) and not input_active:
                    if game.get_game_state() == "come_out":
                        input_active = True
                        message = "Place your bet!"
                        cards = None
                        roll_value = None
                        earnings = None
                    else:
                        result, cards, roll_value = game.play_round()
                        message = result
                        earnings = game.get_bankroll() - previous_bankroll
                        previous_bankroll = game.get_bankroll()

                elif come_out_button.is_clicked(event.pos):
                    if game.get_game_state() == "point":
                        game.set_game_state("come_out")
                        game.reset_point_bets()
                        message = "Starting new round with Come Out roll"
                        input_active = True
                        cards = None
                        roll_value = None
                        earnings = None
                    else:
                        message = "Already in Come Out phase"

                if game.get_game_state() == "point":
                    for value, button in point_bet_buttons.items():
                        if button.is_clicked(event.pos):
                            point_bet_active = True
                            point_bet_input = ""
                            current_point_bet_value = value
                            message = f"Enter point bet amount for {value}"

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        bet_input = bet_input[:-1]
                    else:
                        bet_input += event.unicode
                elif point_bet_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            point_bet = int(point_bet_input)
                            if game.place_point_bet(point_bet, current_point_bet_value):
                                message = f"Point bet of ${point_bet} placed on {current_point_bet_value}"
                            else:
                                message = "Not enough funds for point bet."
                            point_bet_active = False
                        except ValueError:
                            message = "Please enter a valid number."
                        point_bet_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        point_bet_input = point_bet_input[:-1]
                    else:
                        point_bet_input += event.unicode

        come_out_button.update_text("Come Out" if game.get_game_state() == "come_out" else "Point")

        draw_game(screen, game, message, cards, roll_value, earnings)

        if input_active:
            bet_surface = font.render(bet_input, True, BLACK)
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT - 250, 200, 40))
            screen.blit(bet_surface, (WIDTH // 2 - 95, HEIGHT - 245))

        if point_bet_active:
            point_bet_surface = font.render(point_bet_input, True, BLACK)
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT - 300, 200, 40))
            screen.blit(point_bet_surface, (WIDTH // 2 - 95, HEIGHT - 295))

        pygame.display.flip()
        clock.tick(30)

    return  # Return to the main menu

if __name__ == "__main__":
    main()

