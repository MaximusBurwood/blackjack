def update_count(card, running_count):
    """Updates the running count based on the Hi-Lo system."""
    rank = card['rank']
    if rank in ['2', '3', '4', '5', '6']:
        return running_count + 1
    elif rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
        return running_count - 1
    return running_count

def get_true_count(running_count, decks_remaining):
    """Calculates the true count."""
    if decks_remaining <= 0:
        return 0
    return running_count / decks_remaining