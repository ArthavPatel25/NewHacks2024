import pygame
import sys
import os
import random

class DeckManager:
    def __init__(self):
        self.deck = [
            '2_of_clubs', '2_of_diamonds', '2_of_hearts', '2_of_spades',
            '3_of_clubs', '3_of_diamonds', '3_of_hearts', '3_of_spades',
            '4_of_clubs', '4_of_diamonds', '4_of_hearts', '4_of_spades',
            '5_of_clubs', '5_of_diamonds', '5_of_hearts', '5_of_spades',
            '6_of_clubs', '6_of_diamonds', '6_of_hearts', '6_of_spades',
            '7_of_clubs', '7_of_diamonds', '7_of_hearts', '7_of_spades',
            '8_of_clubs', '8_of_diamonds', '8_of_hearts', '8_of_spades',
            '9_of_clubs', '9_of_diamonds', '9_of_hearts', '9_of_spades',
            '10_of_clubs', '10_of_diamonds', '10_of_hearts', '10_of_spades',
            'jack_of_clubs', 'jack_of_diamonds', 'jack_of_hearts', 'jack_of_spades',
            'queen_of_clubs', 'queen_of_diamonds', 'queen_of_hearts', 'queen_of_spades',
            'king_of_clubs', 'king_of_diamonds', 'king_of_hearts', 'king_of_spades',
            'ace_of_clubs', 'ace_of_diamonds', 'ace_of_hearts', 'ace_of_spades'
        ]
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        return None

    def reset_deck(self):
        self.__init__()

    def cards_left(self):
        return len(self.deck)

    

    

#ititialize the game
class Blackjack:
    def __init__(self, screen, player_points,  draw_card_sound_effect, shuffle_card_SF, button_click_SF):
        self.screen = screen
        self.draw_card_sound_effect = draw_card_sound_effect  # Almacena el efecto de sonido
        self.shuffle_card_SF = shuffle_card_SF
        self.button_click_SF = button_click_SF

        self.player_points = player_points
        self.deck = DeckManager()
        self.player_cards = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_card = self.deck.draw_card()
        self.reveal_dealer_cards = False
        self.total_bet = 0  
        self.show_bet_buttons = True 
        self.bet_count = 0 
        self.show_draw_buttons = False

        self.font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 32)
        self.running = True

        self.button_width, self.button_height = 100, 50

        #itialize each button
        self.bet_button_rect = pygame.Rect(
            (screen.get_width() // 2 - self.button_width - 10, screen.get_height() - self.button_height - 20),
            (self.button_width, self.button_height)
        )
        self.quit_button_rect = pygame.Rect(
            (screen.get_width() // 2 + 10, screen.get_height() - self.button_height - 20),
            (self.button_width, self.button_height)
        )
        self.restart_button_rect = pygame.Rect(  
            (screen.get_width() // 2 - self.button_width // 2, screen.get_height() - self.button_height - 80),
            (self.button_width, self.button_height)
        )

        self.draw_button_rect = pygame.Rect(
            (screen.get_width() // 2 - self.button_width - 10, screen.get_height() - self.button_height - 20),
            (self.button_width, self.button_height)
        )
        self.hold_button_rect = pygame.Rect(
            (screen.get_width() // 2 + 10, screen.get_height() - self.button_height - 20),
            (self.button_width, self.button_height)
        )
        self.new_game_button_rect = pygame.Rect(
            (screen.get_width() // 2 - self.button_width // 2, screen.get_height() - self.button_height - 20),
            (self.button_width, self.button_height)
        )

    def load_card_image(self, card_name):
        card_path = os.path.join('images', f"{card_name}.png")
        return pygame.image.load(card_path)
    def reset_game(self):
        self.deck.reset_deck()
        self.bet_count = 0
        self.total_bet = 0
        self.player_cards = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_card = self.deck.draw_card()
        self.show_bet_buttons = True
        self.show_draw_buttons = False
        self.reveal_dealer_cards = False
        self.running = True
        self.shuffle_card_SF.play()

    
    def calculate_score(self):
        score = 0
        aces = 0
        for card in self.player_cards:
            value = card.split('_')[0] 
            if value.isdigit(): 
                score += int(value)
            elif value in ['jack', 'queen', 'king']:
                score += 10
            else: 
                aces += 1
            
        for _ in range(aces):
            if score + 11 > 21:
                score += 1
            else:
                score += 11
            
        return score
    
    def get_card_value(self, card):
        value = card.split('_')[0]  
        if value.isdigit():  
            return int(value)
        elif value in ['jack', 'queen', 'king']:
            return 10
        else:  # Ases
            return 11

    def get_bet_amount(self):
        input_active = True
        user_input = ""
        prompt_text = self.font.render("Bet: ", True, (255, 255, 255))

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            bet_amount = int(user_input)
                            if 0 < bet_amount <= self.player_points:
                                self.player_points -= bet_amount
                                self.total_bet += bet_amount  
                                return self.total_bet, self.player_points
                        except ValueError:
                            user_input = ""

                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

            self.screen.fill((39, 139, 34))
            points_text = self.font.render(f"Points: {self.player_points}", True, (255, 255, 255))
            self.screen.blit(points_text, (self.screen.get_width() - points_text.get_width() - 20, 20))
            self.screen.blit(prompt_text, (self.screen.get_width() // 2 - 50, self.screen.get_height() // 2 - 50))
            user_text = self.font.render(user_input, True, (255, 255, 255))
            self.screen.blit(user_text, (self.screen.get_width() // 2 + 10, self.screen.get_height() // 2 - 50))

            pygame.display.flip()

    def draw_buttons(self):
        if self.show_bet_buttons: 
            pygame.draw.rect(self.screen, (0, 0, 0), self.bet_button_rect, border_radius=5)
            bet_button_text = self.button_font.render("Bet", True, (255, 255, 255))
            self.screen.blit(bet_button_text, (self.bet_button_rect.centerx - bet_button_text.get_width() // 2,
                                                self.bet_button_rect.centery - bet_button_text.get_height() // 2))

            # quit
            pygame.draw.rect(self.screen, (0, 0, 0), self.quit_button_rect, border_radius=5)
            quit_button_text = self.button_font.render("Quit", True, (255, 255, 255))
            self.screen.blit(quit_button_text, (self.quit_button_rect.centerx - quit_button_text.get_width() // 2,
                                                self.quit_button_rect.centery - quit_button_text.get_height() // 2))

            # restart
            pygame.draw.rect(self.screen, (0, 0, 0), self.restart_button_rect, border_radius=5)
            restart_button_text = self.button_font.render("Restart", True, (255, 255, 255))
            self.screen.blit(restart_button_text, (self.restart_button_rect.centerx - restart_button_text.get_width() // 2,
                                                    self.restart_button_rect.centery - restart_button_text.get_height() // 2))
        elif self.show_draw_buttons:  # draw and hold
            pygame.draw.rect(self.screen, (0, 0, 0), self.draw_button_rect, border_radius=5)
            draw_button_text = self.button_font.render("Draw", True, (255, 255, 255))
            self.screen.blit(draw_button_text, (self.draw_button_rect.centerx - draw_button_text.get_width() // 2,
                                                self.draw_button_rect.centery - draw_button_text.get_height() // 2))

            pygame.draw.rect(self.screen, (0, 0, 0), self.hold_button_rect, border_radius=5)
            hold_button_text = self.button_font.render("Hold", True, (255, 255, 255))
            self.screen.blit(hold_button_text, (self.hold_button_rect.centerx - hold_button_text.get_width() // 2,
                                                self.hold_button_rect.centery - hold_button_text.get_height() // 2))
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), self.draw_button_rect, border_radius=5)
            draw_button_text = self.button_font.render("New Game", True, (255, 255, 255))
            self.screen.blit(draw_button_text, (self.draw_button_rect.centerx - draw_button_text.get_width() // 2,
                                                self.draw_button_rect.centery - draw_button_text.get_height() // 2))

            pygame.draw.rect(self.screen, (0, 0, 0), self.hold_button_rect, border_radius=5)
            hold_button_text = self.button_font.render("Quit", True, (255, 255, 255))
            self.screen.blit(hold_button_text, (self.hold_button_rect.centerx - hold_button_text.get_width() // 2,
                                                self.hold_button_rect.centery - hold_button_text.get_height() // 2))


        

    def show_cards(self):
        card_width, card_height = 10, 20  
        # player cards
        for i, card_name in enumerate(self.player_cards):
            card_image = self.load_card_image(card_name)
            x_position = self.screen.get_width() // 4 + i * (card_width + 200)  
            y_position = self.screen.get_height() - card_height - 250
            self.screen.blit(card_image, (x_position, y_position))

        # dealer cards
        if self.reveal_dealer_cards:
            for i, dealer_card in enumerate(self.dealer_cards):
                dealer_card_image = self.load_card_image(dealer_card)
                x_position = self.screen.get_width() // 2 + i * (card_width - 200)
                y_position = -250  
                self.screen.blit(dealer_card_image, (x_position, y_position))
        else:
            dealer_card_image = self.load_card_image(self.dealer_card)
            x_position = self.screen.get_width() // 2 - card_width // 2
            y_position = -250 
            self.screen.blit(dealer_card_image, (x_position, y_position))

    def run(self):
        self.bet_count = 0  
        self.total_bet = 0  
        self.player_cards = []  
        self.dealer_card = None 
        self.shuffle_card_SF.play()




        while self.running:
            if self.bet_count == 0: 
                bet_amount, self.player_points = self.get_bet_amount()
                print(f"Initial bet: {bet_amount}")
                print(f"Points after bet: {self.player_points}")
                self.total_bet = bet_amount 
                self.bet_count += 1  
                
                self.player_cards = [self.deck.draw_card(), self.deck.draw_card()]
                self.dealer_card = self.deck.draw_card()
            
            self.screen.fill((39, 139, 34))
            self.show_cards()  

            points_text = self.font.render(f"Points: {self.player_points}", True, (255, 255, 255))
            self.screen.blit(points_text, (self.screen.get_width() - points_text.get_width() - 20, 20))

            bet_text = self.font.render(f"Total Bet: {self.total_bet}", True, (255, 255, 255))
            self.screen.blit(bet_text, (self.screen.get_width() - bet_text.get_width() - 20, 60))

            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.show_bet_buttons:  
                        if self.quit_button_rect.collidepoint(mouse_pos):
                            self.running = False
                        elif self.bet_button_rect.collidepoint(mouse_pos):
                            self.button_click_SF.play()
                            bet_amount, self.player_points = self.get_bet_amount()
                            print(f"Additional bet: {bet_amount}")
                            print(f"Points after bet: {self.player_points}")

                            # bet logic
                            self.total_bet = bet_amount  
                            self.bet_count += 1 

                            if self.bet_count >= 2:  
                                self.show_bet_buttons = False  
                                self.show_draw_buttons = True

                        elif self.restart_button_rect.collidepoint(mouse_pos):
                            self.button_click_SF.play() 
                            print("Restarting the game...")
                            self.bet_count = 0  
                            self.total_bet = 0 
                            self.player_cards = [] 
                            self.dealer_card = None 
                            self.deck.reset_deck()

                    elif self.show_draw_buttons:  
                        if self.draw_button_rect.collidepoint(mouse_pos):
                            self.button_click_SF.play()
                            #  draw logic
                            new_card = self.deck.draw_card()
                            self.player_cards.append(new_card)
                            print(f"Drew card: {new_card}")
                            self.draw_card_sound_effect.play()

                            player_score = self.calculate_score()
                            if self.player_points <= 0:
                                print("You have no points left! You lose.")
                                self.running = False 
                            print(f"Player score: {player_score}")

                            if player_score > 21:
                                self.show_bet_buttons = False  
                                self.show_draw_buttons = False
                                
                                
                        elif self.hold_button_rect.collidepoint(mouse_pos):
                            self.button_click_SF.play()
                            print("You chose to hold. Finalizing round...")
                            self.dealer_cards = [self.dealer_card]  #First dealer card
                            self.reveal_dealer_cards = True  

                            # dealers logic
                            dealer_score = self.get_card_value(self.dealer_card)
                            while dealer_score < 17:
                                new_dealer_card = self.deck.draw_card()
                                self.dealer_cards.append(new_dealer_card) 
                                dealer_score += self.get_card_value(new_dealer_card)
                                print(f"Dealer drew card: {new_dealer_card}, Score: {dealer_score}")

                            # commpare scores
                            player_score = self.calculate_score()
                            print(f"Player score: {player_score}, Dealer score: {dealer_score}")

                            if dealer_score > 21 or player_score > dealer_score:
                                print("You win! Doubling your bet.")
                                if player_score == 21: #if player gets blackjack, they get 4 times their bet
                                    print("BlackJack")
                                    self.player_points += self.total_bet*2
                                self.player_points += self.total_bet * 2  
                                
                            else:
                                print("You lose! Losing your bet.")
                                if self.player_points <= 0:
                                    print("You have no points left! You lose.")
                                    self.running = False

                            self.show_bet_buttons = False
                            self.show_draw_buttons = False
                    else:
                        if self.new_game_button_rect.collidepoint(mouse_pos):
                            self.button_click_SF.play()
                            print("reseting game")
                            self.reset_game() 
                        if self.quit_button_rect.collidepoint(mouse_pos):
                            self.button_click_SF.play()
                            self.running = False

                                    
            pygame.display.flip()



def run_blackjack(screen,player_points, draw_card_sound_effect, shuffle_card_SF, button_click_SF):
    pygame.init()
    pygame.display.set_caption("Blackjack")
    game = Blackjack(screen, player_points, draw_card_sound_effect, shuffle_card_SF, button_click_SF)
    game.run()


if __name__ == "run_blackjack":
    run_blackjack()