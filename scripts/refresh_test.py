import requests

BASE_URL = "http://localhost:8000"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOThhODRlNy1lNzgwLTRlYmUtOTI0Ny04MGU2NWYxOTY2MGUiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3MTM0MDYzfQ.7DE99bFKWtzkACbMR1OrVc2NL0Cx0wijroeyUartTsE"
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOThhODRlNy1lNzgwLTRlYmUtOTI0Ny04MGU2NWYxOTY2MGUiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NzczODgwM30.JBHjqjxwRCirD282NRe-h-fhWbD-7I4VohleqqpVjg4"

# 2. appel route protégée
headers = {
    "Authorization": f"Bearer {access_token}"
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

if projects_response.status_code == 401:
    refresh_response = requests.post(
        f"{BASE_URL}/users/refresh",
        json={
            "refresh_token": refresh_token
        }
    )
    data = refresh_response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    print("ACCESS TOKEN:", access_token)
    print("REFRESH TOKEN:", refresh_token)

    headers = {
        "Authorization": f"Bearer {access_token}"
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

