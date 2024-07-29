

def sort_by_positions(players):
    lhp = {"position": "Left Handed Pitcher", "players": [],}
    rhp = {"position": "Right Handed Pitcher", "players": [],}
    catcher = {"position": "Catcher", "players": [],}
    infielder = {"position": "Infielder", "players": [],}
    outfielder = {"position": "Outfielder", "players": [],}
    dh = {"position": "Designated Hitter", "players": [],}
    for player in players:
        if player.throws == "Left" and player.position == "Pitcher":
            lhp["players"].append(player)
        elif player.throws == "Right" and player.position == "Pitcher":
            rhp["players"].append(player)
        elif player.position == "Catcher":
            catcher["players"].append(player)
        elif player.position in ["First Base", "Second Base", "Third Base", "Shortstop"]:
            infielder["players"].append(player)
        elif player.position in ["Centerfield", "Corner Outfield"]:
            outfielder["players"].append(player)
        else:
            dh["players"].append(player)
    positions = [lhp, rhp, catcher, infielder, outfielder, dh]
    for position in positions:
        position["count"] = len(position["players"])
    return positions