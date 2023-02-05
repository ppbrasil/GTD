import requests
import random
import string

url = "http://localhost:8000/api/task/create/"
header = {
    "Authorization": "Token 5ff6f6747d1ed186ccb97f611285445dc1bbf4ae",
    "Content-Type": "application/json"
}

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

task = {
    "is_active": True,
    "done": False,
    "focus": False,
    "name": random_string(10),
    "readiness": random.choice(["inbox", "anytime", "waiting", "sometime"]),
    "waiting_for": None,
    "notes": random_string(50),
}

print(f"Task data to be added: {task}")

response = requests.post(url, headers=header, json=task)

if response.status_code == 201:
    print(f"Task successfully created. Content: {response.json()}")
else:
    print(f"Error creating task. Status code: {response.status_code}. Error: {response.json()}")
