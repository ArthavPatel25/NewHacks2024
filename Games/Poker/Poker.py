import os
import sys
import pygame
import random
import traceback

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("Script directory:", os.path.dirname(os.path.abspath(__file__)))
print("Images directory:", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Images')))

# Initialize Pygame
pygame.init()
print("Pygame initialized")

# Set up the display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Professional Poker Game")
print("Display set up successfully")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load images
current_dir = os.path.dirname(__file__)
try:
    table_img = pygame.image.load(os.path.join(current_dir, 'Poker_table.jpg'))
    table_img = pygame.transform.scale(table_img, (WIDTH, HEIGHT))
    print("Table image loaded successfully")
except pygame.error as e:
    print(f"Error loading table image: {e}")
    table_img = pygame.Surface((WIDTH, HEIGHT))
    table_img.fill(GREEN)

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Images'))
        card_path = os.path.join(images_dir, f'{rank}_of_{suit}.png')
        
        try:
            self.image = pygame.image.load(card_path)
            self.image = pygame.transform.scale(self.image, (70, 100))
        except pygame.error as e:
            print(f"Error loading image: {card_path}")
            print(f"Error details: {e}")
            self.image = pygame.Surface((70, 100))
            self.image.fill(RED)
        
        self.back_image = pygame.Surface((70, 100))
        self.back_image.fill(BLUE)
        font = pygame.font.Font(None, 20)
        text = font.render("BACK", True, WHITE)
        text_rect = text.get_rect(center=(35, 50))
        self.back_image.blit(text, text_rect)

        self.is_face_up = False

    def flip(self):
        self.is_face_up = not self.is_face_up

    def draw(self, screen, x, y):
        if self.is_face_up:
            screen.blit(self.image, (x, y))
        else:
            screen.blit(self.back_image, (x, y))

# Player class
class Player:
    def __init__(self, name, chips, position, avatar, is_ai=False):
        self.name = name
        self.chips = chips
        self.position = position
        avatar_path = os.path.join(current_dir, avatar)
        try:
            self.avatar = pygame.image.load(avatar_path)
            self.avatar = pygame.transform.scale(self.avatar, (60, 60))
        except pygame.error as e:
            print(f"Error loading avatar: {avatar_path}")
            print(f"Error details: {e}")
            self.avatar = pygame.Surface((60, 60))
            self.avatar.fill(BLUE)
        self.hand = []
        self.bet = 0
        self.is_active = True
        self.is_ai = is_ai
        self.points = 0

    def make_bet(self, current_bet):
        if self.is_ai:
            return random.randint(current_bet, min(self.chips, current_bet * 2))
        return 0  # Human player will input their bet manually

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Poker Game Logic
class PokerGame:
    def __init__(self):
        self.players = [
            Player("Player 1", 1000, (50, HEIGHT - 150), "player1_avatar.png"),
            Player("Player 2", 1000, (WIDTH - 150, HEIGHT - 150), "player2_avatar.png", is_ai=True),
        ]
        self.host = Player("Host", float('inf'), (WIDTH // 2 - 30, HEIGHT // 2 - 100), "host_avatar.png")
        self.community_cards = []
        self.pot = 0
        self.current_player_index = 0
        self.deck = self.create_deck()
        self.game_state = "preflop"
        self.current_bet = 0

    def create_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        return [Card(suit, rank) for suit in suits for rank in ranks]

    def deal_cards(self):
        random.shuffle(self.deck)
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                card.flip()
                player.hand.append(card)

    def deal_community_cards(self):
        if self.game_state == "preflop":
            for _ in range(3):
                card = self.deck.pop()
                card.flip()
                self.community_cards.append(card)
            self.game_state = "flop"
        elif self.game_state == "flop":
            card = self.deck.pop()
            card.flip()
            self.community_cards.append(card)
            self.game_state = "turn"
        elif self.game_state == "turn":
            card = self.deck.pop()
            card.flip()
            self.community_cards.append(card)
            self.game_state = "river"
        else:
            self.game_state = "showdown"

    def next_player(self):
        if not self.players:
            print("No players in the game")
            return
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"Current player: {self.players[self.current_player_index].name}")

    def handle_action(self, action, amount=0):
        player = self.players[self.current_player_index]
        if action == "fold":
            player.is_active = False
        elif action == "call":
            call_amount = self.current_bet - player.bet
            player.chips -= call_amount
            player.bet += call_amount
            self.pot += call_amount
        elif action == "raise":
            raise_amount = amount - player.bet
            player.chips -= raise_amount
            player.bet += raise_amount
            self.pot += raise_amount
            self.current_bet = amount
        self.next_player()

    def determine_winner(self):
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) == 1:
            return active_players[0]
        elif len(active_players) == 2:
            if self.players[0].bet > self.players[1].bet:
                return self.players[0]
            elif self.players[1].bet > self.players[0].bet:
                return self.players[1]
            else:
                if self.players[0].chips > self.players[1].chips:
                    return self.players[0]
                elif self.players[1].chips > self.players[0].chips:
                    return self.players[1]
                else:
                    return self.players[0]

# Drawing functions
def draw_players(screen, players):
    for player in players:
        x, y = player.position
        screen.blit(player.avatar, (x, y))
        font = pygame.font.Font(None, 24)
        name_text = font.render(player.name, True, WHITE)
        chips_text = font.render(f"${player.chips}", True, WHITE)
        bet_text = font.render(f"Bet: ${player.bet}", True, WHITE)
        screen.blit(name_text, (x + 10, y + 65))
        screen.blit(chips_text, (x + 10, y + 85))
        screen.blit(bet_text, (x + 10, y + 105))
        for i, card in enumerate(player.hand):
            card.draw(screen, x + i * 80, y - 120)

def draw_host(screen, host):
    x, y = host.position
    screen.blit(host.avatar, (x, y))

def draw_community_cards(screen, cards):
    for i, card in enumerate(cards):
        card.draw(screen, WIDTH // 2 - 180 + i * 80, HEIGHT // 2 - 50)

def draw_pot(screen, amount):
    font = pygame.font.Font(None, 36)
    pot_text = font.render(f"Pot: ${amount}", True, WHITE)
    screen.blit(pot_text, (WIDTH // 2 - 50, HEIGHT // 2 - 140))

def draw_points(screen, players):
    font = pygame.font.Font(None, 36)
    player1_text = font.render(f"{players[0].name}: {players[0].points} pts", True, WHITE)
    player2_text = font.render(f"{players[1].name}: {players[1].points} pts", True, WHITE)
    screen.blit(player1_text, (10, 10))
    screen.blit(player2_text, (WIDTH - player2_text.get_width() - 10, 10))

# Main game loop
def main():
    game = PokerGame()
    clock = pygame.time.Clock()
    running = True
    game_state = "playing"
    winner = None

    fold_button = Button(WIDTH // 2 - 230, HEIGHT - 80, 100, 50, "Fold", GREEN)
    call_button = Button(WIDTH // 2 - 100, HEIGHT - 80, 100, 50, "Call", GREEN)
    raise_button = Button(WIDTH // 2 + 30, HEIGHT - 80, 100, 50, "Raise", GREEN)
    quit_button = Button(WIDTH // 2 + 160, HEIGHT - 80, 100, 50, "Quit", GREEN)

    bet_input_box = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 130, 140, 32)
    bet_input = ""
    input_active = False

    game.deal_cards()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "round_over":
                    game = PokerGame()
                    game.deal_cards()
                    game_state = "playing"
                    winner = None
                else:
                    if bet_input_box.collidepoint(event.pos):
                        input_active = not input_active
                    else:
                        input_active = False
                    if fold_button.is_clicked(event.pos):
                        game.handle_action("fold")
                    elif call_button.is_clicked(event.pos):
                        game.handle_action("call")
                    elif raise_button.is_clicked(event.pos):
                        if bet_input:
                            try:
                                bet_amount = int(bet_input)
                                game.handle_action("raise", bet_amount)
                                bet_input = ""
                            except ValueError:
                                print("Invalid bet amount")
                    elif quit_button.is_clicked(event.pos):
                        return  # Ends the Poker game and returns to Main.py
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if bet_input:
                            try:
                                bet_amount = int(bet_input)
                                game.handle_action("raise", bet_amount)
                                bet_input = ""
                            except ValueError:
                                print("Invalid bet amount")
                    elif event.key == pygame.K_BACKSPACE:
                        bet_input = bet_input[:-1]
                    elif event.unicode.isdigit():
                        bet_input += event.unicode

        if game_state == "playing":
            if game.players[game.current_player_index].is_ai:
                ai_bet = game.players[game.current_player_index].make_bet(game.current_bet)
                game.handle_action("raise", ai_bet)

            if game.game_state == "showdown" or len([p for p in game.players if p.is_active]) == 1:
                winner = game.determine_winner()
                winner.points += 50
                game_state = "round_over"

        # Draw everything
        screen.blit(table_img, (0, 0))
        draw_players(screen, game.players)
        draw_host(screen, game.host)
        draw_community_cards(screen, game.community_cards)
        draw_pot(screen, game.pot)
        draw_points(screen, game.players)

        fold_button.draw(screen)
        call_button.draw(screen)
        raise_button.draw(screen)
        quit_button.draw(screen)

        pygame.draw.rect(screen, WHITE, bet_input_box)
        font = pygame.font.Font(None, 32)
        bet_surface = font.render(f"Bet: ${bet_input}", True, BLACK)
        screen.blit(bet_surface, (bet_input_box.x + 5, bet_input_box.y + 5))

        if game_state == "round_over" and winner:
            font = pygame.font.Font(None, 48)
            winner_text = font.render(f"{winner.name} wins!", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            
            font = pygame.font.Font(None, 32)
            continue_text = font.render("Click anywhere to start a new round", True, WHITE)
            screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
