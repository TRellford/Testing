import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playergamelogs
import pandas as pd

@st.cache_data(ttl=3600)
def fetch_player_data(player_name):
    """Fetch player stats from NBA API with error handling."""
    try:
        # Find matching player
        matching_players = [p for p in players.get_players() if p["full_name"].lower() == player_name.lower()]
        
        if not matching_players:
            return {"Error": f"Player '{player_name}' not found."}

        player_id = matching_players[0]["id"]

        # Fetch career stats
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]

        # Fetch game logs
        try:
            game_logs = playergamelogs.PlayerGameLogs(player_id=player_id, season_nullable="2024-25").get_data_frames()[0]
        except Exception:
            return {"Career Stats": career_stats.to_dict(orient="records"), "Game Logs": "No game logs available."}

        # Ensure game logs exist before accessing head()
        if game_logs.empty:
            return {"Career Stats": career_stats.to_dict(orient="records"), "Game Logs": "No game logs available."}

        return {
            "Career Stats": career_stats.to_dict(orient="records"),
            "Last 5 Games": game_logs.head(5).to_dict(orient="records"),
            "Last 10 Games": game_logs.head(10).to_dict(orient="records"),
            "Last 15 Games": game_logs.head(15).to_dict(orient="records")
        }
    
    except Exception as e:
        return {"Error": str(e)}

@st.cache_data(ttl=3600)
def fetch_all_players():
    """Fetch all active NBA players."""
    try:
        return [p["full_name"] for p in players.get_active_players()]
    except Exception as e:
        return {"Error": str(e)}
