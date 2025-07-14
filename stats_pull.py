import requests
import pandas as pd
from dateProcessing import getDateRange


def convert_ip(ip):
    if isinstance(ip, str) and '.' in ip:
        whole, fraction = ip.split('.')
        return int(whole) + int(fraction) / 3
    try:
        return float(ip)
    except:
        return 0.0  # Fallback if value is missing or badly formatted


def safe_division(numerator, denominator):

    try:
        division_value = numerator / denominator
        return division_value

    except ZeroDivisionError:
        return 0


def starting_pitcher_stats(id, date):

    threshold_ip = 15

    default_starting_pitcher = {"averageAgainst": .245,
                                "E_totalBasesAgainst": 101,
                                "E_OPS_Against": .773,
                                "WHIP": 1.32,
                                "pressureDifferential": .415,
                                "ERA": 4.08,
                                "FIP": 4.25,
                                "bb_9": 3.05,
                                "K_BB": 3.07,
                                "team_hr_9": 1.2,
                                "allowed_iso": .217,
                                "contact_outs": 111,
                                "pitches_per_batter": 3.88,
                                "dpi": .695,
                                "ground_air_against": .629,
                                "strand_rate_against": .973}

    starting_pitcher_url = f"https://statsapi.mlb.com/api/v1/people/{id}/stats?stats=byDateRange&group=pitching&startDate=2025-03-27&endDate={date}"
    starting_pitcher_response = requests.get(starting_pitcher_url)
    starting_pitcher_raw_data = starting_pitcher_response.json()

    starting_pitcher_list = []
    starting_pitcher_dict = starting_pitcher_raw_data["stats"][0]["splits"][0]["stat"]
    starting_pitcher_list.append(starting_pitcher_dict)

    pitcherInnings = convert_ip(starting_pitcher_dict["inningsPitched"])

    starting_pitcher_processed = process_pitching_stats(starting_pitcher_list)

    if pitcherInnings < threshold_ip:
        weight = min(1.0, pitcherInnings / threshold_ip)

        for key in starting_pitcher_processed:
            actual = starting_pitcher_processed.get(key,0)
            default = default_starting_pitcher.get(key, 0)
            smoothed_stat = (weight * actual) + ((1 - weight) * default)

            starting_pitcher_processed[key] = smoothed_stat

    return starting_pitcher_processed



def teamTotalStats(team_id, date):

    error_log=[]

    startDate, endDate = getDateRange(date)

    statsURL = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?season=2025&date={endDate}&hydrate=person(stats(group=[hitting,pitching],type=[byDateRange],startDate={startDate},endDate={endDate},season=2025))"
    response_teamStats = requests.get(statsURL)
    total_stats_data = response_teamStats.json()

    team_roster = total_stats_data["roster"]

    pitching_list = []
    batting_list = []

    for player in team_roster:
        try:
            position = player["person"]["primaryPosition"]["code"]
            player_stats = player["person"]["stats"][0]["splits"][0]["stat"]

            if position == "1":
                #add pitcher stats to dictionary and append to pitching_list[]
                pitching_list.append(player_stats)

            else:
                #add batting stats to dictionary and append to batting_list[]
                batting_list.append(player_stats)

        except KeyError:
            player_name = player["person"]["fullName"]
            player_id = player["person"]["id"]
            error_log_entry = f"Player Name: {player_name} ID: {player_id} Team: {team_id} KeyError"
            error_log.append(error_log_entry)
            print(error_log_entry)
            continue

        except IndexError:
            player_name = player["person"]["fullName"]
            player_id = player["person"]["id"]
            error_log_entry = f"Player Name: {player_name} ID: {player_id} Team: {team_id} IndexError"
            error_log.append(error_log_entry)
            continue

    processed_pitching_dict = process_pitching_stats(pitching_list)
    processed_batting_dict = process_batting_stats(batting_list)

    team_dict = {}
    for key, value in processed_pitching_dict.items():
        team_dict[key] = value

    for key, value in processed_batting_dict.items():
        team_dict[key] = value

    return team_dict


def process_pitching_stats(pitching_stats):
    # resolve player pitching stats into team pitching stat list
    # List of Pitching keys to keep
    allowed_keys = [
        "flyOuts","groundOuts","airOuts","runs","doubles","triples","homeRuns","strikeOuts","baseOnBalls",
        "hits","hitByPitch","atBats","caughtStealing","stolenBases","groundIntoDoublePlay", "numberOfPitches",
        "inningsPitched","earnedRuns","battersFaced","outs","gamesPitched","gamesStarted","strikes","hitBatsmen",
        "totalBases","inheritedRunners","inheritedRunnersScored"
    ]

    # Your list of player dictionaries
    filtered_player_dicts = [
        {
            k: convert_ip(v) if k == "inningsPitched" else v
            for k, v in player_dict.items()
            if k in allowed_keys
        }
        for player_dict in pitching_stats
    ]

    pitch_df = pd.DataFrame(filtered_player_dicts)

    team_totals = pitch_df.sum(numeric_only=True)
    team_stat_dict = team_totals.to_dict()

    team_pitch_dict = {}

    team_pitch_dict["averageAgainst"] = safe_division(team_stat_dict["hits"], team_stat_dict["atBats"])
    runners_allowed = team_stat_dict["hits"] + team_stat_dict["hitBatsmen"] + team_stat_dict["baseOnBalls"]
    OBP_against = safe_division(runners_allowed, team_stat_dict["battersFaced"])
    team_pitch_dict["E_totalBasesAgainst"] = team_stat_dict["totalBases"] + team_stat_dict["hitBatsmen"] + team_stat_dict["baseOnBalls"] + team_stat_dict["stolenBases"] - team_stat_dict["caughtStealing"]
    E_slugging_Against = safe_division(team_pitch_dict["E_totalBasesAgainst"], team_stat_dict["battersFaced"])
    team_pitch_dict["E_OPS_Against"] = OBP_against + E_slugging_Against
    team_pitch_dict["WHIP"] = safe_division(runners_allowed, team_stat_dict["inningsPitched"])
    k_inning = safe_division(team_stat_dict["strikeOuts"], team_stat_dict["inningsPitched"])
    team_pitch_dict["pressureDifferential"] = team_pitch_dict["WHIP"] - k_inning
    team_pitch_dict["ERA"] = 9 * safe_division(team_stat_dict["earnedRuns"], team_stat_dict["inningsPitched"])
    fip_numerator = (13 * team_stat_dict["homeRuns"]) + (3 * (team_stat_dict["baseOnBalls"] + team_stat_dict["hitBatsmen"])) - (2 * team_stat_dict["strikeOuts"])
    team_pitch_dict["FIP"] = safe_division(fip_numerator, team_stat_dict["inningsPitched"]) + 3.2
    #team_pitch_dict["hitters_faced_9"] = 9 * safe_division(team_stat_dict["battersFaced"], team_stat_dict["inningsPitched"])
    K_9 = 9 * k_inning
    team_pitch_dict["bb_9"] = 9 * safe_division(team_stat_dict["baseOnBalls"], team_stat_dict["inningsPitched"])
    team_pitch_dict["K_BB"] = safe_division(K_9, team_pitch_dict["bb_9"])
    team_pitch_dict["team_hr_9"] = 9 * safe_division(team_stat_dict["homeRuns"], team_stat_dict["inningsPitched"])
    team_pitch_dict["allowed_iso"] = E_slugging_Against - team_pitch_dict["averageAgainst"]
    team_pitch_dict["contact_outs"] = team_stat_dict["outs"] - team_stat_dict["strikeOuts"]
    team_pitch_dict["pitches_per_batter"] = safe_division(team_stat_dict["numberOfPitches"], team_stat_dict["battersFaced"])
    dpi_numerator = team_stat_dict["battersFaced"] - team_stat_dict["strikeOuts"] - team_stat_dict["baseOnBalls"] - team_stat_dict["hitBatsmen"]
    team_pitch_dict["dpi"] = safe_division(dpi_numerator, team_stat_dict["battersFaced"])
    #team_pitch_dict["reb"] = safe_division(team_stat_dict["runs"], team_stat_dict["battersFaced"])
    total_air_outs = team_stat_dict["airOuts"] + team_stat_dict["flyOuts"]
    team_pitch_dict["ground_air_against"] = safe_division(team_stat_dict["groundOuts"], total_air_outs)
    team_pitch_dict["strand_rate_against"] = 1- safe_division(team_stat_dict["inheritedRunnersScored"], team_stat_dict["inheritedRunners"])

    return team_pitch_dict


def process_batting_stats(batting_stats):
    # resolve player batting stats into team pitching stat list
    # List of Batting keys to keep
    allowed_keys = [
        "gamesPlayed", "flyOuts", "groundOuts", "airOuts", "runs", "doubles", "triples", "homeRuns", "strikeOuts", "baseOnBalls",
        "hits", "hitByPitch", "atBats", "caughtStealing", "stolenBases", "groundIntoDoublePlay", "numberOfPitches",
        "plateAppearances", "totalBases", "rbi", "leftOnBase","sacFlies"
    ]

    # Your list of player dictionaries
    filtered_player_dicts = [
        {k: v for k, v in player_dict.items() if k in allowed_keys}
        for player_dict in batting_stats
    ]

    batting_df = pd.DataFrame(filtered_player_dicts)

    team_totals = batting_df.sum(numeric_only=True)
    team_stat_dict = team_totals.to_dict()

    team_batting_dict = {}

    team_batting_dict["average"] = safe_division(team_stat_dict["hits"], team_stat_dict["atBats"])
    obp_numerator = team_stat_dict["hits"] + team_stat_dict["baseOnBalls"] + team_stat_dict["hitByPitch"]
    team_batting_dict["obp"] = safe_division(obp_numerator, team_stat_dict["plateAppearances"])
    team_batting_dict["E_total_bases"] = team_stat_dict["totalBases"] + team_stat_dict["stolenBases"] + team_stat_dict["baseOnBalls"] + team_stat_dict["hitByPitch"] - team_stat_dict["caughtStealing"]
    E_slugging = safe_division(team_batting_dict["E_total_bases"], team_stat_dict["plateAppearances"])
    team_batting_dict["EOPS"] = team_batting_dict["obp"] + E_slugging
    #team_batting_dict["rbipa"] = safe_division(team_stat_dict["rbi"], team_stat_dict["plateAppearances"])
    team_batting_dict["walkRate"] = safe_division(team_stat_dict["baseOnBalls"], team_stat_dict["plateAppearances"])
    team_batting_dict["kRate"] = safe_division(team_stat_dict["strikeOuts"], team_stat_dict["plateAppearances"])
    team_batting_dict["ktobb"] = safe_division(team_stat_dict["baseOnBalls"], team_stat_dict["strikeOuts"])
    team_batting_dict["E_iso"] = E_slugging - team_batting_dict["average"]
    team_batting_dict["pitches_seen_per_PA"] = safe_division(team_stat_dict["numberOfPitches"], team_stat_dict["plateAppearances"])
    team_batting_dict["runsPerGame"] = safe_division(team_stat_dict["rbi"], team_stat_dict["gamesPlayed"])
    team_batting_dict["homeRunsPerGame"] = safe_division(team_stat_dict["homeRuns"], team_stat_dict["gamesPlayed"])
    team_batting_dict["babip"] = safe_division(team_stat_dict["hits"] - team_stat_dict["homeRuns"], team_stat_dict["atBats"] - team_stat_dict["strikeOuts"] - team_stat_dict["homeRuns"] + team_stat_dict["sacFlies"])
    #team_batting_dict["atBats_hr"] = safe_division(team_stat_dict["atBats"], team_stat_dict["homeRuns"])

    return team_batting_dict
