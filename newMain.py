import requests
import stats_pull
#playerStatsURL = "https://statsapi.mlb.com/api/v1/people/677594/stats?stats=byDateRange&group=hitting&startDate=2025-03-28&endDate=2025-04-07"
#playerStatsURL_2 = "https://statsapi.mlb.com/api/v1/people/677594/stats?stats=byDateRange&group=hitting&startDate=2025-03-28&endDate=2025-06-26"
#playerStatsURL_3 = "https://statsapi.mlb.com/api/v1/teams/111/roster?rosterType=active&date=03/27/2025&hydrate=person(stats(group=[hitting],type=season,season=2025))"

#playerStatsURL = "https://statsapi.mlb.com/api/v1/people/677594/stats?stats=byDateRange&group=hitting&startDate=2025-03-28&endDate=2025-04-07"
#playerStatsURL_3 = "https://statsapi.mlb.com/api/v1/teams/111/roster?rosterType=active&date=03/27/2025&hydrate=person(stats?stats=byDateRange&group=hitting&startDate=2025-03-28&endDate=2025-04-07)"


#goodURL = "https://statsapi.mlb.com/api/v1/teams/111/roster?season=2025&date=06/01/2025&hydrate=person(stats(group=[hitting,pitching],type=[byDateRange],startDate=01/01/2025,endDate=06/01/2025,season=2025))""

#goodURLTeam = "https://statsapi.mlb.com/api/v1/teams/111/stats?group=pitching&season=2025&sportIds=1&stats=byDateRange&startDate=01/01/2025&endDate=06/01/2025"

startDate = "04/27/2025"
endDate = "04/28/2025"
scheduleURL = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date?date=byDateRange&startDate={startDate}&endDate={endDate}&gameType=R&hydrate=team,probablePitcher"

response = requests.get(scheduleURL)
schedule_data = response.json()

schedule_dates = schedule_data["dates"]

games_list = []

for schedule_date in schedule_dates:
    baseball_games = schedule_date["games"]
    for baseball_game in baseball_games:
        game_data = {}
        date = schedule_date["date"]
        team_info = baseball_game["teams"]
        home_team_info = team_info["home"]

        game_data["date"] = date

        game_data["home_team_name"] = home_team_info["team"]["name"]
        game_data["home_team_id"] = home_team_info["team"]["id"]
        game_data["home_team_pitcher_name"] = home_team_info["probablePitcher"]["fullName"]
        game_data["home_team_pitcher_id"] = home_team_info["probablePitcher"]["id"]

        home_team_pitching, home_team_batting = stats_pull.teamTotalStats(home_team_info["team"]["id"], date)


        away_team_info = team_info["away"]

        game_data["away_team_name"] = away_team_info["team"]["name"]
        game_data["away_team_id"] = away_team_info["team"]["id"]
        game_data["away_team_pitcher_name"] = away_team_info["probablePitcher"]["fullName"]
        game_data["away_team_pitcher_id"] = away_team_info["probablePitcher"]["id"]

        game_data["home_team_wins"] = home_team_info["isWinner"]

        games_list.append(game_data)


print(home_team_batting)
print(home_team_pitching)



#response = requests.get(playerStatsURL)
#data = response.json()


#print(data["stats"][0]["splits"][0]["stat"])
#print(data2["stats"][0]["splits"][0]["stat"])