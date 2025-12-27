import requests
import datetime as dt
import config

PIXELA_API_URL = "https://pixe.la/v1/users"
GRAPH_ID = "graph1"

new_user = False

headers = {
    "X-USER-TOKEN": config.PIXELA_TOKEN
}

def create_user():
    params = {
        "token": config.PIXELA_TOKEN,
        "username": config.PIXELA_USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }
    r = requests.post(PIXELA_API_URL, json=params)
    print(r.text)

def create_graph():
    url = f"{PIXELA_API_URL}/{config.PIXELA_USERNAME}/graphs"
    params = {
        "id": GRAPH_ID,
        "name": "Cycling Graph",
        "unit": "Km",
        "type": "float",
        "color": "ajisai"
    }
    r = requests.post(url, json=params, headers=headers)
    print(r.text)

def add_pixel():
    date_input = input("Enter date (YYYY-MM-DD): ")
    km = input("Enter kilometers: ")

    date = dt.datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y%m%d")

    url = f"{PIXELA_API_URL}/{config.PIXELA_USERNAME}/graphs/{GRAPH_ID}"
    params = {
        "date": date,
        "quantity": km
    }
    r = requests.post(url, json=params, headers=headers)
    print(r.text)

if new_user:
    create_user()
    create_graph()
else:
    add_pixel()
