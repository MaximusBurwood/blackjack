import json
from deck import Deck
from hand import Hand
from strategy import get_optimal_move
from card_counter import update_count, get_true_count

class Game:
    def __init__(self, game_state=None):
        if game_state:
            self.deck = Deck(existing_deck=game_state['deck'])
            self.used_cards = game_state['used_cards']
            self.running_count = game_state['running_count']
        else:
            self.deck = Deck(num_decks=6)
            self.used_cards = []
            self.running_count = 0

    def _update_counts_and_state(self, card):
        """Helper to update counts and move card from deck to used pile."""
        self.running_count = update_count(card, self.running_count)
        self.used_cards.append(card)
        self.deck.remove_card(card)

    def play_round(self, player_card1, player_card2, dealer_up_card):
        """Plays a single round of Blackjack."""
        player_hand = Hand()
        player_hand.add_card(player_card1)
        player_hand.add_card(player_card2)

        dealer_hand = Hand()
        dealer_hand.add_card(dealer_up_card)

        # Update state with known cards
        self._update_counts_and_state(player_card1)
        self._update_counts_and_state(player_card2)
        self._update_counts_and_state(dealer_up_card)

        decks_remaining = self.deck.get_decks_remaining()
        true_count = get_true_count(self.running_count, decks_remaining)

        print(f"\nPlayer's hand: {player_hand} (Value: {player_hand.get_value()})")
        print(f"Dealer's up card: {dealer_hand}")
        print(f"Running Count: {self.running_count} | Decks Remaining: {decks_remaining:.2f} | True Count: {true_count:.2f}")

        # Player's turn
        while player_hand.get_value() < 21:
            optimal_move = get_optimal_move(player_hand, dealer_up_card, true_count)
            print(f"Recommended Action: {optimal_move}")

            if optimal_move == 'Stand':
                break
            
            # For this simulation, we assume the player follows the advice.
            # We will only simulate 'Hit' and 'Stand' for simplicity. Double/Split are complex to simulate without more input.
            if optimal_move in ['Hit', 'Double/Hit']:
                new_card = self.deck.deal()
                print(f"Player hits and gets: {new_card['rank']} of {new_card['suit']}")
                self._update_counts_and_state(new_card)
                player_hand.add_card(new_card)
                print(f"Player's new hand: {player_hand} (Value: {player_hand.get_value()})")
            else: # Stand, Double/Stand, Split
                break

        player_value = player_hand.get_value()
        if player_value > 21:
            print("Player busts!")
            return

        # Dealer's turn
        print("\n--- Dealer's Turn ---")
        while dealer_hand.get_value() < 17:
            new_card = self.deck.deal()
            print(f"Dealer hits and gets: {new_card['rank']} of {new_card['suit']}")
            self._update_counts_and_state(new_card)
            dealer_hand.add_card(new_card)
        
        print(f"Dealer's final hand: {dealer_hand} (Value: {dealer_hand.get_value()})")

        dealer_value = dealer_hand.get_value()
        if dealer_value > 21:
            print("Dealer busts! Player wins!")
        elif dealer_value > player_value:
            print(f"Dealer wins with {dealer_value} against player's {player_value}.")
        elif player_value > dealer_value:
            print(f"Player wins with {player_value} against dealer's {dealer_value}.")
        else:
            print("Push (tie).")

    def save_game_state(self):
        """Saves the current game state to a file."""
        game_state = {
            'deck': self.deck.cards,
            'used_cards': self.used_cards,
            'running_count': self.running_count
        }
        with open('game_state.json', 'w') as f:
            json.dump(game_state, f, indent=4)