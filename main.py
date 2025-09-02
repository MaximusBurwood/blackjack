import json
from game import Game

def get_card_from_user(card_name):
    """Gets card rank and suit from the user."""
    ranks = {
        'A': 'Ace', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', 
        '8': '8', '9': '9', '10': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King'
    }
    suits = {
        'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'
    }

    while True:
        rank_input = input(f"Enter the rank for {card_name} (A, 2-10, J, Q, K): ").upper()
        if rank_input in ranks:
            break
        print("Invalid rank. Please try again.")

    while True:
        suit_input = input(f"Enter the suit for {card_name} (H, D, C, S): ").upper()
        if suit_input in suits:
            break
        print("Invalid suit. Please try again.")

    return {'rank': ranks[rank_input], 'suit': suits[suit_input]}

def main():
    """Main function to run the Blackjack game."""
    game = None

    while True:
        if game is None:
            try:
                with open('game_state.json', 'r') as f:
                    game_state = json.load(f)
                game = Game(game_state=game_state)
                print("Continuing with the previous game state.")
            except (FileNotFoundError, json.JSONDecodeError):
                game = Game()
                print("Starting a new game with a fresh shoe.")

        player_card1 = get_card_from_user("your first card")
        player_card2 = get_card_from_user("your second card")
        dealer_up_card = get_card_from_user("the dealer's up card")

        game.play_round(player_card1, player_card2, dealer_up_card)

        while True:
            choice = input("\nChoose an option:\n1. Continue with the same shoe\n2. Start a new game (fresh shoe)\n3. Exit\n> ").strip()
            if choice in ['1', '2', '3']:
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

        if choice == '1':
            game.save_game_state()
        elif choice == '2':
            game = Game()
            game.save_game_state()
            print("\n--- New Game Started ---")
        elif choice == '3':
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()