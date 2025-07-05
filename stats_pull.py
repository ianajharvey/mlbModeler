import requests
from datetime import datetime, timedelta


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

    startDate, endDate = getDateRange(date)

    statsURL = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?season=2025&date={endDate}&hydrate=person(stats(group=[hitting,pitching],type=[byDateRange],startDate={startDate},endDate={endDate},season=2025))"
    response_teamStats = requests.get(statsURL)
    total_stats_data = response_teamStats.json()

    team_roster = total_stats_data["roster"]

    pitching_list = []
    batting_list = []

    for player in team_roster:
        position = player["person"]["primaryPosition"]["code"]

        if position == "1":
            #add pitcher stats to dictionary and append to pitching_list[]

        else:
            #add batting stats to dictionary and append to batting_list[]
