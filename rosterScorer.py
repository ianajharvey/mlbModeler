import statsapi
import pandas as pd

def scoreoffensiveRoster(positionRoster):
    score_dict_list = []
    for player in positionRoster:
        playerDict = {}
        playerCareerStatsRaw = statsapi.player_stat_data(player["ID"],"hitting","career")
        playerCareerStats = playerCareerStatsRaw["stats"][0]["stats"]

        playerDict["Career_hits"] = playerCareerStats["hits"]
        playerDict["Career_doubles"] = playerCareerStats["doubles"]
        playerDict["Career_triples"] = playerCareerStats["triples"]
        playerDict["Career_homeruns"] = playerCareerStats["homeRuns"]
        playerDict["Career_walks"] = playerCareerStats["baseOnBalls"]
        playerDict["Career_hbp"] = playerCareerStats["hitByPitch"]
        playerDict["Career_stolenBases"] = playerCareerStats["stolenBases"]
        playerDict["Career_caughtStealing"] = playerCareerStats["caughtStealing"]
        playerDict["Career_atBats"] = playerCareerStats["atBats"]
        playerDict["Career_plateAppearances"] = playerCareerStats["plateAppearances"]
        playerDict["Career_totalBases"] = playerCareerStats["totalBases"]
        playerDict["Career_rbi"] = playerCareerStats["rbi"]

        score_dict_list.append(playerDict)

    off_df = pd.DataFrame(score_dict_list)

    team_totals = off_df.sum(numeric_only=True)
    team_stat_dict = team_totals.to_dict()

    team_average = team_stat_dict["Career_hits"] / team_stat_dict["Career_atBats"]
    team_obp = (team_stat_dict["Career_hits"] + team_stat_dict["Career_walks"] + team_stat_dict["Career_hbp"]) / team_stat_dict["Career_plateAppearances"]
    team_slugging = team_stat_dict["Career_totalBases"] / team_stat_dict["Career_atBats"]
    team_ops = team_obp + team_slugging
    team_EtotalBases = (team_stat_dict["Career_totalBases"] + team_stat_dict["Career_walks"] + team_stat_dict["Career_hbp"] + team_stat_dict["Career_stolenBases"] - team_stat_dict["Career_caughtStealing"])
    team_Eslugging = team_EtotalBases / team_stat_dict["Career_plateAppearances"]
    team_EOPS = team_Eslugging + team_obp
    team_rbipa = team_stat_dict["Career_rbi"] / team_stat_dict["Career_plateAppearances"]
    team_walkRate = team_stat_dict["Career_walks"] / team_stat_dict["Career_plateAppearances"]
    team_iso = team_slugging - team_average
    team_sbEfficiency = team_stat_dict["Career_stolenBases"] / (team_stat_dict["Career_stolenBases"] + team_stat_dict["Career_caughtStealing"])
    team_Eadvancement = team_EtotalBases / team_stat_dict["Career_plateAppearances"]

    off_dict = {"average": team_average, "obp": team_obp, "slugging": team_slugging, "ops": team_ops,
                "e_totalBases": team_EtotalBases, "e_slugging": team_Eslugging, "e_ops": team_EOPS,
                "rbipa": team_rbipa, "walkRate": team_walkRate, "iso": team_iso, "sb_efficiency":team_sbEfficiency,
                "E+advancement": team_Eadvancement}


    return off_dict


def scorePitchingRoster(pitchingRoster):
    score_dict_list = []
    for player in pitchingRoster:
        playerDict = {}
        playerCareerStatsRaw = statsapi.player_stat_data(player["ID"],"pitching","career")
        playerCareerStats = playerCareerStatsRaw["stats"][0]["stats"]

        playerDict["Career_inningsPitched"] = playerCareerStats["inningsPitched"]
        playerDict["Career_battersFaced"] = playerCareerStats["battersFaced"]
        playerDict["Career_outs"] = playerCareerStats["outs"]
        playerDict["Career_strikeouts"] = playerCareerStats["strikeOuts"]
        playerDict["Career_runs"] = playerCareerStats["runs"]
        playerDict["Career_earnedRuns"] = playerCareerStats["earnedRuns"]
        playerDict["Career_hits"] = playerCareerStats["hits"]
        playerDict["Career_doubles"] = playerCareerStats["doubles"]
        playerDict["Career_triples"] = playerCareerStats["triples"]
        playerDict["Career_homeruns"] = playerCareerStats["homeRuns"]
        playerDict["Career_walks"] = playerCareerStats["baseOnBalls"]
        playerDict["Career_hbp"] = playerCareerStats["hitByPitch"]
        playerDict["Career_stolenBases"] = playerCareerStats["stolenBases"]
        playerDict["Career_caughtStealing"] = playerCareerStats["caughtStealing"]
        playerDict["Career_atBats"] = playerCareerStats["atBats"]
        playerDict["Career_numberOfPitches"] = playerCareerStats["numberOfPitches"]
        playerDict["Career_strikes"] = playerCareerStats["strikes"]
        playerDict["Career_totalBases"] = playerCareerStats["totalBases"]


        score_dict_list.append(playerDict)

    return score_dict_list
