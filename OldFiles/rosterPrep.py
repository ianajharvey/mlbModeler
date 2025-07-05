import statsapi

def rosterPrep(roster_text):
    rosterList = []
    for player in roster_text.strip().split('\n'):
        try:
            parts = player.strip().split(maxsplit=2)
            if len(parts) == 3:
                number = parts[0].lstrip('#')
                position = parts[1]
                name = parts[2]
                playerfull = statsapi.lookup_player(name, season=2025)
                playerID = playerfull[0]["id"]
                rosterList.append({"Number": number, "Position": position, "Name": name, "ID": playerID})
        except IndexError:
            continue

    pitchers = []
    position_players = []

    for player in rosterList:
        if player["Position"] == "P":
            pitchers.append(player)
        else:
            position_players.append(player)

    return position_players,pitchers
