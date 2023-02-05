import requests


url = f"http://localhost:8000/api/task/focused/"
header = {
    "Authorization": "Token 5ff6f6747d1ed186ccb97f611285445dc1bbf4ae",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=header)

if response.status_code == 200:
    print(f"Task successfully retrieved. Content: {response.json()}")
else:
    print(f"Error retrieving task. Status code: {response.status_code}. Error: {response.json()}")
