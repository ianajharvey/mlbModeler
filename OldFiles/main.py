import statsapi
import pandas as pd
import rosterPrep
import rosterScorer
import addPrefixedMetrics

# grab games being looked at
schedule = statsapi.schedule(start_date="03/27/2025",
                        end_date="07/02/2025",
                        team="",
                        opponent="")

gameList = []
gameScores = []
i = 0

for game in schedule:
    try:
        i = i + 1

        game_date = game["game_date"]

        #Grab Home Starting Pitcher Stats
        homePitcher = statsapi.lookup_player(game["home_probable_pitcher"], season=2025)
        homePitcher_ID = homePitcher[0]["id"]
        homePitcherData = []
        homePitcherData.append({"Number": homePitcher[0]["primaryNumber"], "Position": "P", "Name": homePitcher[0]["fullName"], "ID": homePitcher_ID})
        homePitcher_Career_dict = rosterScorer.scorePitchingRoster(homePitcherData, "career")
        homePitcher_Season_dict = rosterScorer.scorePitchingRoster(homePitcherData, "season")

        # Grab Away Starting Pitcher Stats
        awayPitcher = statsapi.lookup_player(game["away_probable_pitcher"], season=2025)
        awayPitcher_ID = awayPitcher[0]["id"]
        awayPitcherData = []
        awayPitcherData.append({"Number": awayPitcher[0]["primaryNumber"], "Position": "P", "Name": awayPitcher[0]["fullName"], "ID": awayPitcher_ID})
        awayPitcher_Career_dict = rosterScorer.scorePitchingRoster(awayPitcherData, "career")
        awayPitcher_Season_dict = rosterScorer.scorePitchingRoster(awayPitcherData, "season")

        homeTeamID = game["home_id"]
        awayTeamID = game["away_id"]

        # Grab team rosters for scoring
        homeRosterList = statsapi.roster(homeTeamID,date=game_date)
        homePositionPlayers, homePitchers = rosterPrep.rosterPrep(homeRosterList)

        # Grab Home batting and pitching data
        homeScoreRoster_Career_Dict = rosterScorer.scoreoffensiveRoster(homePositionPlayers, "career")
        homeScoreRoster_Season_Dict = rosterScorer.scoreoffensiveRoster(homePositionPlayers, "season")
        homeScorePitch_Career_Dict = rosterScorer.scorePitchingRoster(homePitchers, "career")
        homeScorePitch_Season_Dict = rosterScorer.scorePitchingRoster(homePitchers, "season")

        # Grab team rosters for scoring
        awayRosterList = statsapi.roster(awayTeamID, date=game_date)
        awayPositionPlayers, awayPitchers = rosterPrep.rosterPrep(awayRosterList)

        # Grab away batting and pitching data
        awayScoreRoster_Career_Dict = rosterScorer.scoreoffensiveRoster(awayPositionPlayers, "career")
        awayScoreRoster_Season_Dict = rosterScorer.scoreoffensiveRoster(awayPositionPlayers, "season")
        awayScorePitch_Career_Dict = rosterScorer.scorePitchingRoster(awayPitchers, "career")
        awayScorePitch_Season_Dict = rosterScorer.scorePitchingRoster(awayPitchers, "season")

        gamescore = { "Game ID": game["game_id"], "date": game_date, "Field": game["venue_name"],
                     "Home Team": game["home_name"], "Home Pitcher": game["home_probable_pitcher"],
                     "Away Team": game["away_name"], "Away Pitcher": game["away_probable_pitcher"],
                     "Winning Team": game["winning_team"]}

        addPrefixedMetrics.add_prefixed_metrics(gamescore,homePitcher_Career_dict,"home_pitcher_career")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, homePitcher_Season_dict, "home_pitcher_season")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, homeScoreRoster_Career_Dict, "home_batting_career")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, homeScoreRoster_Season_Dict, "home_batting_season")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, homeScorePitch_Career_Dict, "home_bullpen_career")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, homeScorePitch_Season_Dict, "home_bullpen_season")

        addPrefixedMetrics.add_prefixed_metrics(gamescore, awayPitcher_Career_dict, "away_pitcher_career")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, awayPitcher_Season_dict, "away_pitcher_season")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, awayScoreRoster_Career_Dict, "away_batting_career")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, awayScoreRoster_Season_Dict, "away_batting_season")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, awayScorePitch_Career_Dict, "away_bullpen_career")
        addPrefixedMetrics.add_prefixed_metrics(gamescore, awayScorePitch_Season_Dict, "away_bullpen_season")

        gameScores.append(gamescore)
        if i % 10 == 0:
            print(f"processed {i} games")

    except KeyError:
        continue

df = pd.DataFrame(gameScores)

df["Home Team Win"] = df["Home Team"] == df["Winning Team"]

df.to_csv("trainingSet.csv")

# Testing prints
print(df)
