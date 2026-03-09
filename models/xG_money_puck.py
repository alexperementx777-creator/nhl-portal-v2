import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

def update_money_puck_data():
    url = "https://moneypuck.com/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    if not tables:
        return {}
    df = pd.read_html(str(tables[0]))[0]
    
    data = {}
    for _, row in df.iterrows():
        team = str(row.get('Team', '')).strip()
        if team:
            data[team] = {
                "xG_per_60": float(row.get('xG/60', 2.8)),
                "last_updated": datetime.now().isoformat()
            }
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["nhl_portal"]
    db.xg_cache.replace_one({"_id": "current"}, {"data": data, "updated": datetime.now()}, upsert=True)
    return data
