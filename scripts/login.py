from uuid import UUID

import requests

BASE_URL = "http://localhost:8000"

# 1. login
login_response = requests.post(
    f"{BASE_URL}/users/login",
    json={
        "email": "user@example.com",
        "password": "string"
    }
)

data = login_response.json()
access_token = data["access_token"]
refresh_token = data["refresh_token"]

print("ACCESS TOKEN:", access_token)
print("REFRESH TOKEN:", refresh_token)
