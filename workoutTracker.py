import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

APP_ID = os.environ.get("OWN_APP_ID")
API_KEY = os.environ.get("OWN_API_KEY")
API_TOKEN = os.environ.get("OWN_API_TOKEN")
exercise_api_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_api_endpoint = os.environ.get("SHEET_ENDPOINT")



Exercise_question = input("Tell me what exercise you did today?")

exercise_params = {
    "query": Exercise_question,
    "gender": "female",
    "weight_kg": 51,
    "height_cm": 167.64,
    "age": 20
}
header = {
    "x-app-key": API_KEY,
    "x-app-id": APP_ID,
}
response = requests.post(url=exercise_api_endpoint, json=exercise_params, headers=header)
exercises = response.json()


today = datetime.now()
now_time = datetime.time(today).strftime("%H:%M:%S")

for exercise in exercises["exercises"]:
    daily_params = {
        'workout': {
            "date": today.strftime(f"%d{'/'}%m{'/'}%Y"),
            "time": now_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']

        }
    }

    basic = HTTPBasicAuth(
        os.environ.get("USERNAME"),
        os.environ.get("PASSWORD")
    )

    sheet_response = requests.post(
        url=sheety_api_endpoint,
        json=daily_params,
        auth=basic
    )
    print(sheet_response.text)
