import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import fetch_player_data, fetch_all_players

# Fetch all player names once and store in session state
if "player_list" not in st.session_state:
    st.session_state["player_list"] = fetch_all_players()

# Function to filter players based on input
def filter_players(search_input):
    if not search_input:
        return []
    return [name for name in st.session_state["player_list"] if search_input.lower() in name.lower()]

# User types name, and we dynamically update suggestions
search_input = st.text_input("Search for a Player:", "")
filtered_players = filter_players(search_input)

# If matches are found, let the user select from them
if filtered_players:
    player_name = st.selectbox("Select a Player:", filtered_players)
else:
    player_name = None

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
            # Convert to DataFrame and remove the first column
            df = pd.DataFrame(game_logs)[["GAME_DATE", "PTS", "REB", "AST", "FG_PCT", "FG3M"]]

            # Ensure numerical formatting
            df["FG_PCT"] = df["FG_PCT"].round(2)  # FG% to 2 decimal places

            # Set index starting at 1 instead of 0
            df.index = range(1, len(df) + 1)

            # Display stats table
            st.subheader(f"{selected_games} Stats")
            st.dataframe(df)

            # Plot the stats (excluding "Minutes")
            st.subheader(f"{selected_games} Performance Graph")
            fig, ax = plt.subplots(figsize=(10, 5))
            df.set_index("GAME_DATE")[["PTS", "REB", "AST", "FG_PCT", "FG3M"]].plot(kind='bar', ax=ax)
            ax.set_title(f"{player_name} - {selected_games}")
            ax.set_xlabel("Game Date")
            ax.set_ylabel("Stats")
            ax.legend(loc="upper right")
            plt.xticks(rotation=45)
            st.pyplot(fig)
