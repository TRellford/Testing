import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playergamelogs
import pandas as pd

@st.cache_data(ttl=3600)
def fetch_player_data(player_name):
    """Fetch player stats from NBA API with proper game log retrieval."""
    try:
        # Find matching player
        matching_players = [p for p in players.get_players() if p["full_name"].lower() == player_name.lower()]
        
        if not matching_players:
            return {"Error": f"Player '{player_name}' not found."}

        player_id = matching_players[0]["id"]

        # Fetch career stats
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]

        # Fetch game logs for the 2024-25 season using the correct parameter
        try:
            game_logs = playergamelogs.PlayerGameLogs(player_id_nullable=player_id, season_nullable="2024-25").get_data_frames()[0]
        except Exception as e:
            return {
                "Career Stats": career_stats.to_dict(orient="records"),
                "Last 5 Games": [],
                "Last 10 Games": [],
                "Error": f"Failed to retrieve game logs: {str(e)}"
            }

        # Ensure game logs exist
        if game_logs.empty:
            return {
                "Career Stats": career_stats.to_dict(orient="records"),
                "Last 5 Games": [],
                "Last 10 Games": [],
                "Error": "No recent game data available for the 2024-25 season."
            }

        # Select key stats for display (remove "MIN")
        stat_columns = ["GAME_DATE", "PTS", "REB", "AST", "FG_PCT", "FG3M"]

        # Convert game logs to only relevant columns
        game_logs_filtered = game_logs[stat_columns]

        # Convert date column to a readable format
        game_logs_filtered["GAME_DATE"] = pd.to_datetime(game_logs_filtered["GAME_DATE"]).dt.strftime('%Y-%m-%d')

        # Format numerical values
        game_logs_filtered["FG_PCT"] = game_logs_filtered["FG_PCT"].round(2)  # FG% to 2 decimal places

        # Structure output data
        return {
            "Career Stats": career_stats.to_dict(orient="records"),
            "Last 5 Games": game_logs_filtered.head(5).to_dict(orient="records"),
            "Last 10 Games": game_logs_filtered.head(10).to_dict(orient="records"),
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

def fetch_head_to_head_stats(player_name, opponent_team):
    """Fetch head-to-head stats of a player vs. a specific opponent."""
    try:
        matching_players = [p for p in players.get_players() if p["full_name"].lower() == player_name.lower()]
        
        if not matching_players:
            return {"Error": f"Player '{player_name}' not found."}

        player_id = matching_players[0]["id"]

        # Fetch last 10 games and filter by opponent
        game_logs = playergamelogs.PlayerGameLogs(player_id_nullable=player_id, season_nullable="2024-25").get_data_frames()[0]
        
        h2h_games = game_logs[game_logs["MATCHUP"].str.contains(opponent_team, na=False, case=False)]
        
        if h2h_games.empty:
            return {"Error": f"No head-to-head games found vs. {opponent_team}."}

        return h2h_games.to_dict(orient="records")

    except Exception as e:
        return {"Error": str(e)}
