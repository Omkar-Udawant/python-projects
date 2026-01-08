import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")


class DataManager:

    def __init__(self):
        self._user = os.getenv("SHEETY_USERNAME")
        self._password = os.getenv("SHEETY_PASSWORD")

        if not self._user or not self._password:
            raise ValueError("Sheety credentials missing in .env")

        self._auth = HTTPBasicAuth(self._user, self._password)
        self.destination_data = []

    def get_destination_data(self):
        response = requests.get(
            url=SHEETY_PRICES_ENDPOINT,
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self._auth
            )
            response.raise_for_status()
