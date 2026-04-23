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

projects_response = requests.post(
    f"{BASE_URL}/projects",
    headers=headers,
    json={
    "address": "123 Main Street, New York",
    "name": "New Project"
    }
)

print("STATUS:", projects_response.status_code)
print("DATA:", projects_response.json())