import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import fetch_player_data, fetch_all_players

# Streamlit UI
st.title("NBA Player Search")

# Input for player name
player_name = st.text_input("Enter Player Name:", "")

# Optional selector for H2H stats
team_list = [""] + ["ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", 
                     "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", 
                     "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", 
                     "TOR", "UTA", "WAS"]

selected_team = st.selectbox("Optional: Select Opponent for Head-to-Head Stats", team_list)

# Search button
if st.button("Search") and player_name:
    with st.spinner("Fetching player data..."):
        player_data = fetch_player_data(player_name)

    # Handle errors
    if "Error" in player_data:
        st.error(player_data["Error"])
    else:
        # Radio button for game logs selection (default to last 5 games)
        selected_games = st.radio("Select Number of Games to Display:", ["Last 5 Games", "Last 10 Games", "Last 15 Games"], index=0)

        # Display selected game logs
        game_logs = player_data[selected_games]
        st.subheader(f"{selected_games} Stats")
        st.dataframe(game_logs)

        # Convert to DataFrame
        df = pd.DataFrame(game_logs)

        # Ensure numerical columns are selected
        numeric_columns = df.select_dtypes(include=['number']).columns

        # Plot the stats
        if not df.empty:
            st.subheader(f"{selected_games} Performance Graph")
            fig, ax = plt.subplots(figsize=(10, 5))
            df[numeric_columns].plot(kind='bar', ax=ax)
            ax.set_title(f"{player_name} - {selected_games}")
            ax.set_xlabel("Game Index")
            ax.set_ylabel("Stats")
            ax.legend(loc="upper right")
            st.pyplot(fig)

        # Display H2H stats if team selected
        if selected_team:
            with st.spinner(f"Fetching head-to-head stats vs. {selected_team}..."):
                h2h_stats = fetch_head_to_head_stats(player_name, selected_team)  # Function to be added in utils.py
            if "Error" in h2h_stats:
                st.error(h2h_stats["Error"])
            else:
                st.subheader(f"Head-to-Head Stats vs. {selected_team}")
                st.dataframe(h2h_stats)
