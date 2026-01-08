import requests
import os
from dotenv import load_dotenv

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"



class FlightSearch:

    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_SECRET")
        print("API Key:", self._api_key)
        print("API Secret:", self._api_secret)
        self._token = self._get_new_token()

    def _get_new_token(self):
        response = requests.post(
            url=TOKEN_ENDPOINT,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self._api_key,
                "client_secret": self._api_secret,
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params={
                "keyword": city_name,
                "max": 1,
                "include": "AIRPORTS",
            },
        )
        try:
            return response.json()["data"][0]["iataCode"]
        except (IndexError, KeyError):
            return "N/A"

    def check_flights(self, origin, destination, from_time, to_time):
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params={
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": from_time.strftime("%Y-%m-%d"),
                "returnDate": to_time.strftime("%Y-%m-%d"),
                "adults": 1,
                "nonStop": "true",
                "currencyCode": "GBP",
                "max": 10,
            },
        )

        if response.status_code != 200:
            return None

        return response.json()
