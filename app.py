import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
        selected_games = st.radio("Select Number of Games to Display:", ["Last 5 Games", "Last 10 Games", "Last 15 Games"], index=0)

        # Display selected game logs
        game_logs = player_data.get(selected_games, [])

        if not game_logs:
            st.warning(f"No game data available for {selected_games}.")
        else:
            # Display stats table
            st.subheader(f"{selected_games} Stats")
            st.dataframe(game_logs)

            # Convert to DataFrame
            df = pd.DataFrame(game_logs)

            # Ensure numerical columns are selected
            numeric_columns = ["PTS", "REB", "AST", "FG_PCT", "FG3M", "MIN"]
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

            # Plot the stats
            if not df.empty:
                st.subheader(f"{selected_games} Performance Graph")
                fig, ax = plt.subplots(figsize=(10, 5))
                df.set_index("GAME_DATE")[numeric_columns].plot(kind='bar', ax=ax)
                ax.set_title(f"{player_name} - {selected_games}")
                ax.set_xlabel("Game Date")
                ax.set_ylabel("Stats")
                ax.legend(loc="upper right")
                plt.xticks(rotation=45)
                st.pyplot(fig)
