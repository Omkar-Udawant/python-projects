import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
one_month_from_today = datetime.now() + timedelta(days=30)

for destination in sheet_data:
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        tomorrow,
        one_month_from_today
    )


    cheapest_flight = find_cheapest_flight(flights)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        notification_manager.send_whatsapp(
            f"Low price alert! £{cheapest_flight.price} "
            f"from {cheapest_flight.origin_airport} "
            f"to {cheapest_flight.destination_airport} "
            f"{cheapest_flight.out_date} - {cheapest_flight.return_date}"
        )
