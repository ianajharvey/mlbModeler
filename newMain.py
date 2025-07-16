import requests
import dictionaryProcessing
import stats_pull
import pandas as pd

startDate = "04/27/2025"
endDate = "07/07/2025"
scheduleURL = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date?date=byDateRange&startDate={startDate}&endDate={endDate}&gameType=R&hydrate=team,probablePitcher"

response = requests.get(scheduleURL)
schedule_data = response.json()

schedule_dates = schedule_data["dates"]

games_list = []

i = 0

for schedule_date in schedule_dates:
    baseball_games = schedule_date["games"]
    for baseball_game in baseball_games:
        try:
            i = i + 1

            game_data = {}
            date = schedule_date["date"]
            game_data["date"] = date

            team_info = baseball_game["teams"]

            home_team_info = team_info["home"]
            game_data["home_team_name"] = home_team_info["team"]["name"]
            game_data["home_team_id"] = home_team_info["team"]["id"]
            game_data["home_team_pitcher_name"] = home_team_info["probablePitcher"]["fullName"]
            home_pitcher_ID = home_team_info["probablePitcher"]["id"]
            game_data["home_team_pitcher_id"] = home_pitcher_ID

            away_team_info = team_info["away"]
            game_data["away_team_name"] = away_team_info["team"]["name"]
            game_data["away_team_id"] = away_team_info["team"]["id"]
            game_data["away_team_pitcher_name"] = away_team_info["probablePitcher"]["fullName"]
            away_pitcher_ID = away_team_info["probablePitcher"]["id"]
            game_data["away_team_pitcher_id"] = away_pitcher_ID

            home_team_dict = stats_pull.teamTotalStats(home_team_info["team"]["id"], date)
            home_starting_pitcher_dict = stats_pull.starting_pitcher_stats(home_pitcher_ID, date)

            away_team_dict = stats_pull.teamTotalStats(away_team_info["team"]["id"], date)
            away_starting_pitcher_dict = stats_pull.starting_pitcher_stats(away_pitcher_ID, date)

            team_matchup_dict = dictionaryProcessing.head_to_head_stats(home_team_dict, away_team_dict)
            pitcher_matchup_dict = dictionaryProcessing.head_to_head_stats(home_starting_pitcher_dict,away_starting_pitcher_dict)

            dictionaryProcessing.add_prefixed_metrics(game_data, team_matchup_dict, "Team_")
            dictionaryProcessing.add_prefixed_metrics(game_data, pitcher_matchup_dict, "Pitcher_")

            game_data["home_team_wins"] = home_team_info["isWinner"]

            games_list.append(game_data)

            if i % 10 == 0:
                print(f"processed {i} games")

        except KeyError:
            continue

df = pd.DataFrame(games_list)
df.to_csv("trainingSet.csv")