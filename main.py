from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import uvicorn
from models.monte_carlo import run_monte_carlo
from models.xG_money_puck import update_money_puck_data
from models.nhl_api import get_todays_games

app = FastAPI(title="NHL Portal v2.0")

client = MongoClient("mongodb://localhost:27017")
db = client["nhl_portal"]
archive = db["archive"]

app.mount("/static", StaticFiles(directory="frontend"), name="static")

class MatchInput(BaseModel):
    match: str
    prediction: str

@app.post("/analyze")
async def analyze_match(data: MatchInput):
    xg_data = update_money_puck_data()
    mc_prob = run_monte_carlo(2.85, 2.65)
    final_prob = round(mc_prob * 0.7 + 55, 1)

    result = {
        "date": datetime.now().strftime("%d.%m.%Y"),
        "match": data.match,
        "prediction": data.prediction,
        "probability": f"{final_prob}%",
        "result": "—"
    }
    archive.insert_one(result)
    return result

@app.get("/today")
async def today_games():
    return get_todays_games()

@app.get("/archive")
async def get_archive():
    return list(archive.find({}, {"_id": 0}))

@app.get("/")
async def home():
    with open("frontend/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
