# Weather API Service 🌦️

## Overview
A simple FastAPI project that fetches weather data from OpenWeather API, stores it in SQLite, and provides REST endpoints.

## Features
- Fetch live weather data by city
- Save history in SQLite database
- Retrieve past weather records
- Auto-generated API docs via Swagger

## Endpoints
- `GET /{cityname}` → Fetch & store weather
- `GET /history/{cityname}` → Get stored history

## Run Locally
```bash
uvicorn main:app --reload
