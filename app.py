from fastapi import FastAPI, Depends
import requests
from sqlalchemy.orm import Session
from models import Base, Weather
from database import SessionLocal, engine


app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/")
def root():
    return {"message": "This is test line"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/weather/{cityname}")
def get_weather(cityname: str, db: Session = Depends(get_db)):
    api_key = "3fa7c1db032b6282a5643b8392b1e327"
    limit = 5
    location = requests.get(
        "http://api.openweathermap.org/geo/1.0/direct",
        params={"q": cityname, "limit": limit, "appid": api_key},
    )
    geo_loc = location.json()
    lat = geo_loc[0]["lat"]
    lon = geo_loc[0]["lon"]

    weather = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
    )

    data = weather.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["description"]

    weather_entry = Weather(
        city=cityname, temperature=temperature, humidity=humidity, condition=condition
    )

    db.add(weather_entry)
    db.commit()
    db.refresh(weather_entry)

    return {
        "city": cityname.capitalize(),
        "temperature": str(temperature) + " C",
        "humidity": str(humidity) + "%",
        "condition": condition.title(),
    }


@app.get("/history/{cityname}")
def get_history(cityname: str, db: Session = Depends(get_db)):
    rows = db.query(Weather).filter(Weather.city == cityname).all()
    return rows


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    rows = db.query(Weather).all()
    return rows
