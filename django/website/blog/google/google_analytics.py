from datetime import datetime
import json
import os
import requests
import uuid

def track_conversion():
    # Google Analytics 4 Measurement Protocol endpoint
    endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={os.environ.get('GOOGLE_ANALYTICS_ID')}&api_secret={os.environ.get('GA_4_MP_SECRET')}"

    # Google Analytics 4 parameters
    payload = {
    "client_id": str(uuid.uuid4()),
    "non_personalized_ads": False,
    "events": [
            {
                "name": "phone_call",
            }
        ]
    }

    response = requests.post(endpoint, data=json.dumps(payload),verify=True)

    if response.ok:
        print("Conversion tracked successfully")
    else:
        print("Failed to track conversion. Status code:", response.status_code)