import statsapi

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

    return score_dict_list


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
