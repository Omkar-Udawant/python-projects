class FlightData:

    def __init__(self, price, origin, destination, out_date, return_date):
        self.price = price
        self.origin_airport = origin
        self.destination_airport = destination
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data):
    # Check if the "data" key exists and has any items
    if not data or "data" not in data or not data["data"]:
        print("No flight data returned:", data)
        return FlightData(price="N/A", origin=None, destination=None, out_date=None, return_date=None)

    # Now we know data["data"] has at least one element, so it's safe to access it
    cheapest = data["data"][0]
    lowest_price = float(cheapest["price"]["grandTotal"])

    return FlightData(
        price=lowest_price,
        origin=cheapest["itineraries"][0]["segments"][0]["departure"]["iataCode"],
        destination=cheapest["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
        out_date=cheapest["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0],
        return_date=cheapest["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0],
    )
