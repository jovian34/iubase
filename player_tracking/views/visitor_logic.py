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


def group_drafted_player(draft_year, player):
    if player.hsgrad_year == int(draft_year):
        player.group = "High School Signee"
    else:
        player.group = "IU Player/Alumni"


def set_drafted_player(draft_year, player, trans):
    player.drafted = True
    player.position = trans.primary_position
    player.draft_round = trans.draft_round
    player.prof_org = trans.prof_org.__str__()
    player.slot = trans.bonus_or_slot
    player.draft_comment = trans.comment 
    group_drafted_player(draft_year, player)


def set_signed_player(player, trans):
    player.signed = True
    player.bonus = trans.bonus_or_slot
    player.sign_comment = trans.comment
    player.bonus_pct = 100 * player.bonus / player.slot


def set_draft_combine_player_props(draft_year, player, trans):
    player.combine = True
    player.position = trans.primary_position   
    if player.hsgrad_year == int(draft_year):
        player.group = "Freshman"
    else:
        player.group = "College"