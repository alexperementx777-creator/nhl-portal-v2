import requests
from datetime import date

def get_todays_games():
    today = date.today().isoformat()
    url = f"https://statsapi.web.nhl.com/api/v1/schedule?date={today}"
    response = requests.get(url)
    data = response.json()
    
    games = []
    for game in data.get('dates', [{}])[0].get('games', []):
        games.append({
            "match": f"{game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']}",
            "time": game['gameDate'][11:16]
        })
    return games
