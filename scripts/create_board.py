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

project_id = "6190d411-2861-450f-9a01-7a1dfe9a6b22"

boards_response = requests.post(
    f"{BASE_URL}/projects/{project_id}/boards",
    headers=headers,
    json={
        "name": "New board",
        "parent_id": "29a55acc-cd85-4914-9ef6-89f0c3936daf"
    }
)

print("STATUS:", boards_response.status_code)
print("DATA:", boards_response.json())