import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# -------------------- CONFIGURATION -------------------- #

# Load environment variables
load_dotenv()

OWM_API_KEY = os.getenv("OWM_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
TARGET_NUMBER = os.getenv("TARGET_NUMBER")

# Location coordinates
MY_LAT = 37.7550636464
MY_LONG = 14.995246019

# Number of hours to check (max 48 for free tier)
TIME_SPAN = 12

# OpenWeather One Call API (3.0)
OWM_API_URL = "https://api.openweathermap.org/data/2.5/forecast"



# -------------------- FUNCTIONS -------------------- #

def get_weather_data():
    """Fetch weather forecast data (free API version)."""
    params = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "appid": OWM_API_KEY
    }

    response = requests.get(OWM_API_URL, params=params)
    response.raise_for_status()

    data = response.json()
    return data.get("list", [])


def will_rain(forecast_data):
    """Check if rain is expected in the next TIME_SPAN hours."""

    # Each item is 3 hours apart
    checks = TIME_SPAN // 3

    for item in forecast_data[:checks]:
        weather_id = int(item["weather"][0]["id"])

        if 200 <= weather_id < 600:
            return True

    return False


def send_sms_alert():
    """Send SMS alert using Twilio."""
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        message = client.messages.create(
            body="🌧️ Rain expected in the next few hours. Don't forget your umbrella!",
            from_=TWILIO_NUMBER,
            to=TARGET_NUMBER
        )

        print(f"SMS sent successfully. Status: {message.status}")

    except TwilioRestException as error:
        print("Failed to send SMS.")
        print(error)


# -------------------- MAIN EXECUTION -------------------- #

def main():
    try:
        hourly_data = get_weather_data()

        if not hourly_data:
            print("No weather data received.")
            return

        if will_rain(hourly_data):
            print("Rain detected. Sending SMS alert...")
            send_sms_alert()
        else:
            print("No rain expected in the next 12 hours.")

    except requests.exceptions.RequestException as error:
        print("Weather API request failed.")
        print(error)


if __name__ == "__main__":
    main()

