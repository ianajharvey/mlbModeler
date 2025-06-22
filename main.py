import statsapi
import pandas as pd

schedule = statsapi.schedule(start_date="03/27/2025",
                        end_date="03/27/2025",
                        team="147",
                        opponent="")

gameList = []
gameScores = []

for game in schedule:
    homePitcher = statsapi.lookup_player(game["home_probable_pitcher"])
    homePitcher_ID = homePitcher[0]["id"]

    awayPitcher = statsapi.lookup_player(game["away_probable_pitcher"])
    awayPitcher_ID = awayPitcher[0]["id"]

    gamescore = {"Home Team": game["home_name"],"Home ID": game["home_id"],
                 "Home Pitcher": game["home_probable_pitcher"], "Home Pitcher ID": homePitcher_ID, "Home Score": game["home_score"],
                 "Away Team": game["away_name"],"Away ID": game["away_id"],
                 "Away Pitcher": game["away_probable_pitcher"], "Away Pitcher ID": awayPitcher_ID, "Away Score": game["away_score"],
                 "Field": game["venue_name"], "Field ID": game["venue_id"], "Game ID": game["game_id"],
                 "Winning Team": game["winning_team"]}
    gameScores.append(gamescore)

    gameList.append(game["game_id"])

df = pd.DataFrame(gameScores)

df["Home Team Win"] = df["Home Team"] == df["Winning Team"]

print(df)
