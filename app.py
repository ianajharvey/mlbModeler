import pandas as pd
import streamlit as st
from datetime import date

today = date.today()
today_string = today.strftime("%m/%d/%Y")

game_predictions = pd.read_csv("data/predictions/prediction_master.csv")

# Melt to long format for the models
model_conf_cols = ["Log_Reg_Preds", "XGB_Preds", "RF_Preds", "Ensemble_Preds"]
df_long = game_predictions.melt(
    id_vars=[
        "date", "home_team_name", "home_team_id", "home_team_pitcher_name", "home_team_pitcher_id",
        "away_team_name", "away_team_id", "away_team_pitcher_name", "away_team_pitcher_id"
    ],
    value_vars=model_conf_cols,
    var_name="model_name",
    value_name="home_win_confidence"
)

df_long["model_name"] = df_long["model_name"].str.replace("_Preds", "").replace({
    "Log_Reg": "Logistic Regression",
    "XGB": "XGBoost",
    "RF": "Random Forest",
    "Ensemble": "Ensemble"
})

df_long["predicted_winner"] = df_long["home_win_confidence"].apply(lambda x: "Home" if x >= 0.5 else "Away")

base_logo_url = "https://www.mlbstatic.com/team-logos/team-cap-on-light/"

df_long["home_team_logo"] = df_long["home_team_id"].apply(lambda x: f"{base_logo_url}{x}.svg")
df_long["away_team_logo"] = df_long["away_team_id"].apply(lambda x: f"{base_logo_url}{x}.svg")

#Todays Date at the tops
st.header(f"Schedule for {today_string}")

# Dropdown to select model
model_to_display = st.selectbox("Choose a model", df_long["model_name"].unique())

# Filter for selected model
filtered_df = df_long[df_long["model_name"] == model_to_display]

# Display game predictions
for idx, row in filtered_df.iterrows():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(row["home_team_logo"], width=80)
        st.caption(row["home_team_name"])

    with col2:
        confidence = row["home_win_confidence"]
        home_pct = int(confidence * 100)
        away_pct = 100 - home_pct
        bar_html = f"""
        <div style='display: flex; align-items: center;'>
            <div style='background-color: #004687; height: 25px; width: {home_pct}%; text-align: left; color: white; padding-left: 5px; border-radius: 4px 0 0 4px;'>
            </div>
            <div style='background-color: #c8102e; height: 25px; width: {away_pct}%; text-align: right; color: white; padding-right: 5px; border-radius: 0 4px 4px 0;'>
            </div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)
        st.caption(f"Confidence: {home_pct}% Home / {away_pct}% Away")

    with col3:
        st.image(row["away_team_logo"], width=80)
        st.caption(row["away_team_name"])

    st.markdown("---")
