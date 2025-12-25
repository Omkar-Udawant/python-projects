import requests

API_URL = "https://opentdb.com/api.php"
PARAMS = {"amount": 12, "type": "boolean", "category": 18}

offline_data = [
    {"question": "Linus Torvalds created Linux and Git.", "correct_answer": "True"},
    {"question": "Python is based on JavaScript.", "correct_answer": "False"},
    {"question": "RAM stands for Random Access Memory.", "correct_answer": "True"},
    {"question": "Ada Lovelace was the first programmer.", "correct_answer": "True"}
]

def load_data():
    try:
        response = requests.get(API_URL, params=PARAMS, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["results"] if data["response_code"] == 0 else offline_data
    except:
        return offline_data
