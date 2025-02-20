import requests

# Your API key
api_key = "4c9fcd3030eac22e83179bf85a0cee0b"

# Example endpoint: Get NBA odds for US region, moneyline market
url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/"
params = {
    "apiKey": api_key,  # Case matters—keep it as "apiKey"
    "regions": "us",    # US bookmakers (e.g., DraftKings, FanDuel)
    "markets": "h2h",   # Head-to-head (moneyline) odds
    "oddsFormat": "american",  # American odds (-110, +150, etc.)
    "dateFormat": "iso"  # ISO timestamps
}

# Make the GET request
response = requests.get(url, params=params)

# Check the response
if response.status_code == 200:
    data = response.json()
    print("Success! Here’s the first game’s data:")
    print(data[0])  # Prints the first game’s odds
else:
    print(f"Error {response.status_code}: {response.text}")
