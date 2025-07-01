import statsapi
import pandas as pd
import rosterPrep
import rosterScorer

# grab games being looked at
schedule = statsapi.schedule(start_date="03/27/2025",
                        end_date="03/27/2025",
                        team="147",
                        opponent="")

gameList = []
gameScores = []

for game in schedule:
    # grab starting pitchers for weighted scoring
    game_date = game["game_date"]

    #Grab Home Starting Pitcher Stats
    homePitcher = statsapi.lookup_player(game["home_probable_pitcher"], season=2025)
    homePitcher_ID = homePitcher[0]["id"]
    homePitcherData = []
    homePitcherData.append({"Number": homePitcher[0]["primaryNumber"], "Position": "P", "Name": homePitcher[0]["fullName"], "ID": homePitcher_ID})
    homePitcher_dict = rosterScorer.scorePitchingRoster(homePitcherData, "career")

    # Grab Away Starting Pitcher Stats
    awayPitcher = statsapi.lookup_player(game["away_probable_pitcher"], season=2025)
    awayPitcher_ID = awayPitcher[0]["id"]
    awayPitcherData = []
    awayPitcherData.append({"Number": awayPitcher[0]["primaryNumber"], "Position": "P", "Name": awayPitcher[0]["fullName"], "ID": awayPitcher_ID})
    awayPitcher_dict = rosterScorer.scorePitchingRoster(awayPitcherData, "career")

    homeTeamID = game["home_id"]
    awayTeamID = game["away_id"]

    # Grab team rosters for scoring
    homeRosterList = statsapi.roster(homeTeamID,date=game_date)
    homePositionPlayers, homePitchers = rosterPrep.rosterPrep(homeRosterList)

    # Grab Home batting and pitching data
    homeScoreRosterDict = rosterScorer.scoreoffensiveRoster(homePositionPlayers, "career")
    homeScorePitchDict = rosterScorer.scorePitchingRoster(homePitchers, "career")

    # Grab team rosters for scoring
    awayRosterList = statsapi.roster(awayTeamID, date=game_date)
    awayPositionPlayers, awayPitchers = rosterPrep.rosterPrep(awayRosterList)

    # Grab away batting and pitching data
    awayScoreRosterDict = rosterScorer.scoreoffensiveRoster(awayPositionPlayers, "career")
    awayScorePitchDict = rosterScorer.scorePitchingRoster(awayPitchers, "career")

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

# Testing prints
print(schedule)
print(homePitcher_dict)
print(awayPitcher_dict)
print(homeScoreRosterDict)
print(homeScorePitchDict)
print(awayScoreRosterDict)
print(awayScorePitchDict)