import streamlit as st
import pandas as pd
from utils import fetch_player_data, fetch_all_players

# Streamlit UI
st.title("NBA Player Search")

# Input for player name
player_name = st.text_input("Enter Player Name:", "")

# Search button
if st.button("Search") and player_name:
    with st.spinner("Fetching player data..."):
        player_data = fetch_player_data(player_name)
        st.session_state["player_data"] = player_data  # Store in session state

# Retrieve data from session state (if available)
if "player_data" in st.session_state:
    player_data = st.session_state["player_data"]

    if "Error" in player_data:
        st.error(player_data["Error"])
    else:
        # Radio button for selecting the number of games to display
        selected_games = st.radio("Select Number of Games to Display:", ["Last 5 Games", "Last 10 Games"], index=0)

        # Display selected game logs
        game_logs = player_data.get(selected_games, [])

        if not game_logs:
            st.warning(f"No game data available for {selected_games}.")
        else:
            # Select only relevant columns (remove "MIN")
            df = pd.DataFrame(game_logs)[["GAME_DATE", "PTS", "REB", "AST", "FG_PCT", "FG3M"]]

            # Ensure numerical formatting
            df["FG_PCT"] = df["FG_PCT"].round(2)  # FG% to 2 decimal places

            # Display stats table
            st.subheader(f"{selected_games} Stats")
            st.dataframe(df)
