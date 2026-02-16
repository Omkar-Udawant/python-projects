# 🌧️ Weather Alert Automation

A Python project that checks the hourly weather forecast using the OpenWeather API and sends an SMS alert via Twilio if rain is expected in the next 12 hours.

## 🚀 Features
- Fetches hourly weather data
- Detects rain conditions
- Sends SMS notification
- Uses environment variables for security

## 🛠 Tech Stack
- Python
- OpenWeather API
- Twilio API
- requests
- python-dotenv

## ⚙️ Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
```
OWM_API_KEY=your_api_key
TWILIO_SID=your_sid
TWILIO_TOKEN=your_token
TWILIO_NUMBER=your_twilio_number
TARGET_NUMBER=your_phone_number
```

3. Run the script:
```bash
python main.py
```

If rain is detected, you will receive an SMS alert.

