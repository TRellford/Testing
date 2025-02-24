import streamlit as st
from utils import fetch_player_data, fetch_all_players

# Streamlit UI
st.title("NBA Player Search")

# Input field for player name
player_name = st.text_input("Enter Player Name:", "")

# Search button
if st.button("Search") and player_name:
    with st.spinner("Fetching player data..."):
        player_data = fetch_player_data(player_name)

    # Handle Errors
    if "Error" in player_data:
        st.error(player_data["Error"])
    else:
        # Display Career Stats
        st.subheader("Career Stats")
        st.dataframe(player_data["Career Stats"])

        # Display Last 5, 10, 15 Games
        for key in ["Last 5 Games", "Last 10 Games", "Last 15 Games"]:
            if key in player_data:
                st.subheader(key)
                st.dataframe(player_data[key])
            else:
                st.warning(f"{key} data is not available.")
