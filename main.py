import statsapi
import pandas as pd

schedule = statsapi.schedule(start_date="03/27/2025",
                        end_date="06/18/2025",
                        team="",
                        opponent="")


gameScores = []

for game in schedule:
    gamescore = {"Home Team": game["home_name"],"Home ID": game["home_id"], "Home Score": game["home_score"],
                 "Away Team": game["away_name"],"Away ID": game["away_id"], "Away Score": game["away_score"]}
    gameScores.append(gamescore)

df = pd.DataFrame(gameScores)

print(df)
#print(statsapi.get('team', {'teamId':143}))