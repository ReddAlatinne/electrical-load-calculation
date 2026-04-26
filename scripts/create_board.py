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
token = data["access_token"]

print("TOKEN:", token)

# 2. appel route protégée
headers = {
    "Authorization": f"Bearer {token}"
}

project_id = "46d8e168-8e1b-4b11-abfa-8e597a49fdd4"

boards_response = requests.post(
    f"{BASE_URL}/projects/{project_id}/boards",
    headers=headers,
    json={
        "name": "New board",
        "parent_id": "aa35f6c3-38bf-47c1-8c83-5e4177b4c713"
    }
)

print("STATUS:", boards_response.status_code)
print("DATA:", boards_response.json())