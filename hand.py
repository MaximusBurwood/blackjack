class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            rank = card['rank']
            if rank in ['Jack', 'Queen', 'King', '10']:
                value += 10
            elif rank == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(rank)
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def is_pair(self):
        return len(self.cards) == 2 and self.cards[0]['rank'] == self.cards[1]['rank']

    def is_soft(self):
        value = 0
        aces = 0
        for card in self.cards:
            rank = card['rank']
            if rank == 'Ace':
                aces += 1
                value += 11
            elif rank in ['Jack', 'Queen', 'King', '10']:
                value += 10
            else:
                value += int(rank)
        
        # It's a soft hand if an Ace is counted as 11 without busting
        return aces > 0 and value <= 21

    def __str__(self):
        return ', '.join([f"{card['rank']} of {card['suit']}" for card in self.cards])