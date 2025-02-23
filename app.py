import streamlit as st
from datetime import datetime, timedelta
from utils import get_games_by_date  # Assuming utils.py is in the same directory

# Set page config
st.set_page_config(page_title="NBA Games Test", layout="wide")

# Header
st.header("🏀 NBA Games Fetch Test")

# Date selection
base_date = datetime.date.today()
date_option = st.radio("Choose Game Date:", ["Today's Games", "Tomorrow's Games", "Custom Date"], key="test_date")

if date_option == "Today's Games":
    game_date = base_date
elif date_option == "Tomorrow's Games":
    game_date = base_date + timedelta(days=1)
else:
    game_date = st.date_input("Select a Date", value=base_date, min_value=base_date - timedelta(days=365), max_value=base_date + timedelta(days=365))

# Fetch games
available_games = get_games_by_date(game_date.strftime('%Y-%m-%d'))

# Display results
st.write(f"📅 Fetching games for: {game_date.strftime('%Y-%m-%d')}")
st.write(f"🎮 Number of games found: {len(available_games)}")

if available_games:
    st.subheader("Games Found:")
    for game in available_games:
        st.write(f"{game['home_team']} vs {game['away_team']} (Game ID: {game['game_id']})")
else:
    st.warning("🚨 No NBA games found for the selected date. Check the debugging output above for details.")
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
