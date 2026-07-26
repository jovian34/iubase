def calculate_outside_indiana_percentage(players):
    home_states = [player.home_state for player in players if player.home_state]
    if not home_states:
        return 0
    outside_indiana_count = sum(state != "IN" for state in home_states)
    return round(outside_indiana_count / len(home_states) * 100)
