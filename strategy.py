import csv

# Load strategy charts on startup
BASIC_STRATEGY = {}
with open('basic_strategy.csv', mode='r') as infile:
    reader = csv.reader(infile)
    next(reader) # Skip header
    for row in reader:
        BASIC_STRATEGY[row[0]] = {str(i): move for i, move in enumerate(row[1:], 2)}
        BASIC_STRATEGY[row[0]]['10'] = row[9]
        BASIC_STRATEGY[row[0]]['A'] = row[10]

DEVIATIONS = {}
with open('strategy_deviations.csv', mode='r') as infile:
    reader = csv.reader(infile)
    next(reader) # Skip header
    for player_hand, dealer_card, true_count, move in reader:
        key = (player_hand, dealer_card)
        if key not in DEVIATIONS:
            DEVIATIONS[key] = []
        DEVIATIONS[key].append({'tc': int(true_count), 'move': move})

def get_optimal_move(player_hand, dealer_up_card, true_count):
    """
    Determines the optimal move by checking for True Count deviations
    first, then defaulting to basic strategy.
    """
    player_value = player_hand.get_value()
    dealer_rank = dealer_up_card['rank']
    if dealer_rank in ['Jack', 'Queen', 'King']:
        dealer_rank = '10'
    elif dealer_rank == 'Ace':
        dealer_rank = 'A'

    # 1. Determine hand type and create lookup key
    hand_key = ""
    if player_hand.is_pair():
        rank = player_hand.cards[0]['rank']
        rank_val = '10' if rank in ['Jack', 'Queen', 'King'] else 'A' if rank == 'Ace' else rank
        hand_key = f"P{rank_val},{rank_val}"
    elif player_hand.is_soft():
        hand_key = f"S{player_value}"
    else: # Hard total
        hand_key = f"H{player_value}"

    # 2. Check for strategy deviations based on True Count
    deviation_key = (str(player_value), dealer_rank)
    if deviation_key in DEVIATIONS:
        for dev in sorted(DEVIATIONS[deviation_key], key=lambda x: x['tc'], reverse=True):
            if true_count >= dev['tc']:
                return dev['move'] # Return the deviated move

    # 3. If no deviation applies, use basic strategy
    if hand_key in BASIC_STRATEGY:
        return BASIC_STRATEGY[hand_key][dealer_rank]
    
    # Fallback for values not in the chart (e.g., > 21, which shouldn't happen here)
    if player_value >= 17: return 'Stand'
    return 'Hit'