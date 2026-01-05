import requests
import os
from datetime import datetime

# ---------------- USER INPUT ----------------
gender = input("Please enter your gender (male/female): ").strip().lower()
weight_kg = float(input("Please enter your weight in kg: "))
height_cm = float(input("Please enter your height in cm: "))
age = int(input("Please enter your age: "))
exercise_text = input("Tell me which exercises you did: ")

# ---------------- ENV VARIABLES ----------------
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]
SHEETY_ENDPOINT = os.environ["ENV_SHEETY_ENDPOINT"]
SHEETY_TOKEN = os.environ["ENV_SHEETY_TOKEN"]

# ---------------- NUTRITION API ----------------
nutrition_url = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"

headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

data = {
    "query": exercise_text,
    "gender": gender,
    "weight_kg": weight_kg,
    "height_cm": height_cm,
    "age": age
}

response = requests.post(nutrition_url, headers=headers, json=data)
result = response.json()

# ---------------- DATE & TIME ----------------
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# ---------------- SAVE TO GOOGLE SHEETS ----------------
for exercise in result.get("exercises", []):
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        SHEETY_ENDPOINT,
        json=sheet_inputs,
        auth=(
            os.environ["ENV_SHEETY_USERNAME"],
            os.environ["ENV_SHEETY_PASSWORD"]
        )
    )

    print(sheet_response.text)
