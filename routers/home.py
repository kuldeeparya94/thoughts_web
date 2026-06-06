import httpx, os
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
API_KEY = os.getenv("OPENWEATHER_KEY")

@router.get("/{city}")
async def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params={"q": city, "appid": API_KEY, "units": "metric"})
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="City not found")
    data = r.json()
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }