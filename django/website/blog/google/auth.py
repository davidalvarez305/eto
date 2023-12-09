import json
import os
from pathlib import Path
import requests
from oauth2client.client import OAuth2Credentials


def get_auth():
    google_secrets_file = os.environ.get('GOOGLE_JSON_PATH')
    f = open(google_secrets_file)
    data = json.load(f)

    client_id = data['web']['client_id']
    client_secret = data['web']['client_secret']
    token_uri = data['web']['token_uri']
    refresh_token = str(os.environ.get('GOOGLE_API_REFRESH_TOKEN'))

    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_uri, params=params)

    creds = response.json()

    credentials = OAuth2Credentials(
        access_token=creds['access_token'],
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        token_expiry=creds['expires_in'],
        token_uri=token_uri,
        user_agent=str(os.environ.get('GOOGLE_API_USER_AGENT')),
        scopes=creds['scope'],
    )

    return credentials