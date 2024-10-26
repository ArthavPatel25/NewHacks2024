import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import random
from Games.Utility.utility import DeckManager

class CrapsGame:
    def __init__(self):
        self.deck_manager = DeckManager()
        self.player_bankroll = 1000  # Starting bankroll
        self.current_bet = 0
        self.point = 0
        self.game_state = "come_out"  # "come_out" or "point"

    def place_bet(self, amount):
        if amount <= self.player_bankroll:
            self.current_bet = amount
            self.player_bankroll -= amount
            return True
        return False

    def roll_dice(self):
        # Instead of rolling dice, we'll draw two cards and use their values
        self.deck_manager.shuffle_deck()
        card1 = self.deck_manager.draw_card()
        card2 = self.deck_manager.draw_card()
        
        if card1 is None or card2 is None:
            self.deck_manager.reset_deck()
            return self.roll_dice()
        
        value1 = self.card_to_value(card1)
        value2 = self.card_to_value(card2)
        return value1 + value2, (card1, card2)

    def card_to_value(self, card):
        # Convert card to a value between 1 and 6
        value = card.split('_')[0]
        if value in ['jack', 'queen', 'king']:
            return 6
        elif value == 'ace':
            return 1
        else:
            return min(int(value) // 2, 6)  # Ensure maximum value is 6

    def play_round(self):
        if self.game_state == "come_out":
            return self.come_out_roll()
        else:
            return self.point_roll()

    def come_out_roll(self):
        roll, cards = self.roll_dice()
        if roll in [7, 11]:
            self.win()
            return f"Natural {roll}! You win!", cards
        elif roll in [2, 3, 12]:
            self.lose()
            return f"Craps {roll}! You lose.", cards
        else:
            self.point = roll
            self.game_state = "point"
            return f"Point is {roll}", cards

    def point_roll(self):
        roll, cards = self.roll_dice()
        if roll == self.point:
            self.win()
            self.game_state = "come_out"
            return f"You made the point {roll}! You win!", cards
        elif roll == 7:
            self.lose()
            self.game_state = "come_out"
            return "Seven out! You lose.", cards
        else:
            return f"Rolled {roll}, point is {self.point}", cards

    def win(self):
        self.player_bankroll += self.current_bet * 2
        self.current_bet = 0

    def lose(self):
        self.current_bet = 0

    def get_bankroll(self):
        return self.player_bankroll

    def get_game_state(self):
        return self.game_state

    def get_point(self):
        return self.point

# Example usage:
if __name__ == "__main__":
    game = CrapsGame()
    while game.get_bankroll() > 0:
        bet = int(input(f"Your bankroll is ${game.get_bankroll()}. Place your bet: "))
        if game.place_bet(bet):
            result, cards = game.play_round()
            print(f"You rolled: {cards[0]} and {cards[1]}")
            print(result)
            print(f"Your bankroll is now ${game.get_bankroll()}")
        else:
            print("Invalid bet amount.")
        
        if input("Play another round? (y/n): ").lower() != 'y':
            break
    
    print(f"Game over. Final bankroll: ${game.get_bankroll()}")