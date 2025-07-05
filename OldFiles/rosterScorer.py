import statsapi
import pandas as pd

def scoreoffensiveRoster(positionRoster):
    score_dict_list = []
    for player in positionRoster:
        try:
            playerDict = {}
            playerStatsRaw = statsapi.player_stat_data(player["ID"],"hitting", "season")
            playerStats = playerStatsRaw["stats"][0]["stats"]

            playerDict["hits"] = playerStats["hits"]
            playerDict["doubles"] = playerStats["doubles"]
            playerDict["triples"] = playerStats["triples"]
            playerDict["homeruns"] = playerStats["homeRuns"]
            playerDict["walks"] = playerStats["baseOnBalls"]
            playerDict["hbp"] = playerStats["hitByPitch"]
            playerDict["stolenBases"] = playerStats["stolenBases"]
            playerDict["caughtStealing"] = playerStats["caughtStealing"]
            playerDict["atBats"] = playerStats["atBats"]
            playerDict["plateAppearances"] = playerStats["plateAppearances"]
            playerDict["totalBases"] = playerStats["totalBases"]
            playerDict["rbi"] = playerStats["rbi"]

            score_dict_list.append(playerDict)

        except IndexError:
            continue


    off_df = pd.DataFrame(score_dict_list)

    team_totals = off_df.sum(numeric_only=True)
    team_stat_dict = team_totals.to_dict()

    team_average = team_stat_dict["hits"] / team_stat_dict["atBats"]
    team_obp = (team_stat_dict["hits"] + team_stat_dict["walks"] + team_stat_dict["hbp"]) / team_stat_dict["plateAppearances"]
    team_slugging = team_stat_dict["totalBases"] / team_stat_dict["atBats"]
    team_ops = team_obp + team_slugging
    team_EtotalBases = (team_stat_dict["totalBases"] + team_stat_dict["walks"] + team_stat_dict["hbp"] + team_stat_dict["stolenBases"] - team_stat_dict["caughtStealing"])
    team_Eslugging = team_EtotalBases / team_stat_dict["plateAppearances"]
    team_EOPS = team_Eslugging + team_obp
    team_rbipa = team_stat_dict["rbi"] / team_stat_dict["plateAppearances"]
    team_walkRate = team_stat_dict["walks"] / team_stat_dict["plateAppearances"]
    team_iso = team_slugging - team_average
    team_sbEfficiency = team_stat_dict["stolenBases"] / (team_stat_dict["stolenBases"] + team_stat_dict["caughtStealing"])
    team_Eadvancement = team_EtotalBases / team_stat_dict["plateAppearances"]

    off_dict = {"average": team_average, "e_ops": team_EOPS, "rbipa": team_rbipa, "iso": team_iso, "E_advancement": team_Eadvancement}


    return off_dict


def scorePitchingRoster(pitchingRoster, type):
    score_dict_list = []
    for player in pitchingRoster:
        try:
            playerDict = {}
            playerStatsRaw = statsapi.player_stat_data(player["ID"],"pitching",type)
            playerStats = playerStatsRaw["stats"][0]["stats"]

            playerDict["inningsPitched"] = convert_innings_pitched(playerStats["inningsPitched"])
            playerDict["battersFaced"] = playerStats["battersFaced"]
            playerDict["outs"] = playerStats["outs"]
            playerDict["strikeouts"] = playerStats["strikeOuts"]
            playerDict["runs"] = playerStats["runs"]
            playerDict["earnedRuns"] = playerStats["earnedRuns"]
            playerDict["hits"] = playerStats["hits"]
            playerDict["doubles"] = playerStats["doubles"]
            playerDict["triples"] = playerStats["triples"]
            playerDict["homeruns"] = playerStats["homeRuns"]
            playerDict["walks"] = playerStats["baseOnBalls"]
            playerDict["hbp"] = playerStats["hitByPitch"]
            playerDict["stolenBases"] = playerStats["stolenBases"]
            playerDict["caughtStealing"] = playerStats["caughtStealing"]
            playerDict["atBats"] = playerStats["atBats"]
            playerDict["numberOfPitches"] = playerStats["numberOfPitches"]
            playerDict["strikes"] = playerStats["strikes"]
            playerDict["totalBases"] = playerStats["totalBases"]
            playerDict["gamesPitched"] = playerStats["gamesPitched"]
            playerDict["gamesStarted"] = playerStats["gamesStarted"]
            playerDict["groundOuts"] = playerStats["groundOuts"]
            playerDict["airOuts"] = playerStats["airOuts"]


            score_dict_list.append(playerDict)

        except IndexError:
            continue


    pitch_df = pd.DataFrame(score_dict_list)

    team_totals = pitch_df.sum(numeric_only=True)
    team_stat_dict = team_totals.to_dict()

    if team_stat_dict["inningsPitched"] != 0:
        team_whip = (team_stat_dict["hits"] + team_stat_dict["walks"] + team_stat_dict["hbp"]) / team_stat_dict["inningsPitched"]
        team_k_per_inning = team_stat_dict["strikeouts"] / team_stat_dict["inningsPitched"]
        team_pressure_differential = team_whip - team_k_per_inning
        team_ERA = 9 * team_stat_dict["earnedRuns"] / team_stat_dict["inningsPitched"]
        team_FIP = (((13 * team_stat_dict["homeruns"]) + (3 * (team_stat_dict["walks"] + team_stat_dict["hbp"])) - (
                    2 * team_stat_dict["strikeouts"])) / team_stat_dict["inningsPitched"]) + 3.2
        team_hitters_faced_9 = (team_stat_dict["battersFaced"] / team_stat_dict["inningsPitched"]) * 9
        team_k_9 = team_k_per_inning * 9
        team_bb_9 = (team_stat_dict["walks"] / team_stat_dict["inningsPitched"]) * 9
        team_hr_9 = (team_stat_dict["homeruns"] / team_stat_dict["inningsPitched"]) * 9
    team_allowed_average = team_stat_dict["hits"] / team_stat_dict["atBats"]
    team_allowed_OBP = (team_stat_dict["hits"] + team_stat_dict["walks"] + team_stat_dict["hbp"]) / team_stat_dict["battersFaced"]
    team_allowed_slugging = team_stat_dict["totalBases"] / team_stat_dict["atBats"]
    team_allowed_OPS = team_allowed_OBP + team_allowed_slugging
    team_allowed_E_Slugging = (team_stat_dict["totalBases"] + team_stat_dict["walks"]+ team_stat_dict["hbp"] + team_stat_dict["stolenBases"] - team_stat_dict["caughtStealing"]) / team_stat_dict["battersFaced"]
    team_allowed_EOPS = team_allowed_OBP + team_allowed_E_Slugging

    team_k_bb = team_stat_dict["strikeouts"] / team_stat_dict["walks"]

    team_allowed_iso = team_allowed_slugging - team_allowed_average
    team_contact_outs = team_stat_dict["outs"] - team_stat_dict["strikeouts"]
    team_pitches_per_batter = team_stat_dict["numberOfPitches"] / team_stat_dict["battersFaced"]
    team_dpi = (team_stat_dict["battersFaced"] - team_stat_dict["strikeouts"] - team_stat_dict["walks"] - team_stat_dict["hbp"]) / team_stat_dict["battersFaced"]
    team_reb = team_stat_dict["runs"] / team_stat_dict["battersFaced"]
    team_ground_air = team_stat_dict["groundOuts"] / team_stat_dict["airOuts"]
    team_innings_game = team_stat_dict["inningsPitched"] / team_stat_dict["gamesPitched"]

    pitch_dict = {"ERA": team_ERA, "FIP":team_FIP, "PDiff": team_pressure_differential, "KBB": team_k_bb,
                  "EOPSAgainst": team_allowed_EOPS, "Hittersper9":team_hitters_faced_9, "ISOAgainst": team_allowed_iso,
                  "ContactOuts": team_contact_outs, "DPI": team_dpi, "REB": team_reb, "GroundtoAir": team_ground_air}

    return pitch_dict

def convert_innings_pitched(innings_str):
    try:
        if '.' in innings_str:
            parts = innings_str.split('.')
            whole_innings = int(parts[0])
            outs = int(parts[1])
            if outs not in [0, 1, 2]:
                raise ValueError("Invalid number of outs in inning string")
            return whole_innings + (outs / 3)
        else:
            return float(innings_str)
    except (ValueError, TypeError):
        return None  # or raise an error/log it

