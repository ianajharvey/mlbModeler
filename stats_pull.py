import requests
from datetime import datetime, timedelta
import pandas


def getDateRange(end_date):
    # Define the date format
    date_format = "%Y-%m-%d"
    new_date_format = "%m/%d/%Y"
    # Parse the input string into a datetime object
    original_date = datetime.strptime(end_date, date_format)

    # Subtract 20 days
    date_20_days_before = original_date - timedelta(days=20)

    # Convert date back to string format
    start_date = date_20_days_before.strftime(new_date_format)

    return start_date, end_date



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
            print(error_log_entry)
            continue

    return pitching_list, batting_list


def process_pitching_stats(pitching_stats):
    # resolve player pitching stats into team pitching stat list
    # List of Pitching keys to keep
    allowed_keys = [
        "flyOuts","groundOuts","airOuts","runs","doubles","triples","homeRuns","strikeOuts","baseOnBalls",
        "hits","hitByPitch","atBats","caughtStealing","stolenBases","groundIntoDoublePlay", "numberOfPitches",
        "inningsPitched","earnedRuns","battersFaced","Outs","gamesPitched","gamesStarted","strikes","hitsBatsmen",
        "totalBases","inheritedRunners","inheritedRunnersScored"
    ]

    # Your list of player dictionaries
    filtered_player_dicts = [
        {k: v for k, v in player_dict.items() if k in allowed_keys}
        for player_dict in pitching_stats
    ]

def process_batting_stats(batting_stats):
    # resolve player batting stats into team pitching stat list
    # List of Batting keys to keep
    allowed_keys = [
        "gamesPlayed", "flyOuts", "groundOuts", "airOuts", "runs", "doubles", "triples", "homeRuns", "strikeOuts", "baseOnBalls",
        "hits", "hitByPitch", "atBats", "caughtStealing", "stolenBases", "groundIntoDoublePlay", "numberOfPitches",
        "plateAppearances", "totalBases", "rbi", "leftOnBase"
    ]

    # Your list of player dictionaries
    filtered_player_dicts = [
        {k: v for k, v in player_dict.items() if k in allowed_keys}
        for player_dict in batting_stats
    ]