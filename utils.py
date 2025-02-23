import pandas as pd  # Add this if not already present
from nba_api.stats.endpoints import scoreboardv2

@st.cache_data(ttl=3600)
def get_games_by_date(date):
    """Fetch only NBA games for a specific date from the NBA API."""
    if isinstance(date, str):
        date_str = date
    else:
        date_str = date.strftime("%Y-%m-%d")

    try:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=date_str)
        data_frames = scoreboard.get_data_frames()

        # Debugging: Check what the API returns
        st.write(f"📋 DataFrames returned for {date_str}: {len(data_frames)}")
        if not data_frames:
            st.warning(f"🚨 No data returned from API for {date_str}. Possibly no games scheduled or API issue.")
            print(f"🚨 No data returned from API for {date_str}")
            return []

        # Safely access the first DataFrame, default to empty if unavailable
        games_data = data_frames[0] if data_frames else pd.DataFrame()
        st.write("🔍 GameHeader DataFrame:", games_data)

        if games_data.empty:
            st.warning(f"🚨 No games found for {date_str}. This might be due to the All-Star break or no scheduled games.")
            print(f"🚨 No games found for {date_str}")
            return []

        # Filter NBA games (LEAGUE_ID '00' for NBA)
        nba_games = games_data[games_data["LEAGUE_ID"] == "00"]
        if nba_games.empty:
            st.warning(f"🚨 No NBA games (LEAGUE_ID '00') found for {date_str}.")
            print(f"🚨 No NBA games found for {date_str}")
            return []

        formatted_games = [
            {
                "home_team": row["HOME_TEAM_NAME"],
                "away_team": row["VISITOR_TEAM_NAME"],
                "game_id": row["GAME_ID"],
                "date": row["GAME_DATE"]
            }
            for _, row in nba_games.iterrows()
        ]
        st.write(f"✅ Found {len(formatted_games)} NBA games for {date_str}")
        return formatted_games

    except Exception as e:
        st.error(f"❌ Error fetching games for {date_str}: {e}")
        print(f"❌ Error fetching games for {date_str}: {e}")
        return []
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
