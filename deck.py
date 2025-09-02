import random

class Deck:
    def __init__(self, num_decks=6, existing_deck=None):
        self.num_decks = num_decks
        if existing_deck is not None:
            self.cards = existing_deck
        else:
            self.cards = self.create_deck()
            self.shuffle()

    def create_deck(self):
        """Creates a multi-deck shoe."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [{'rank': rank, 'suit': suit} for _ in range(self.num_decks) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise ValueError("The deck is empty!")
        return self.cards[0] # Deal from the top without removing yet

    def remove_card(self, card_to_remove):
        """Explicitly removes a known card from the deck."""
        try:
            self.cards.remove(card_to_remove)
        except ValueError:
            # This can happen if the user enters a card that's already been "used" in a previous session
            print(f"Warning: Card {card_to_remove} not found in deck. It may have already been played.")

    def get_decks_remaining(self):
        """Calculates the number of 52-card decks remaining in the shoe."""
        return len(self.cards) / 52.0