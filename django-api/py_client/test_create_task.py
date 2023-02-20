import requests
import random
import string


create_url = "http://localhost:8000/api/task/create/"

header = {
    "Authorization": "Token c6c1b11be4d99d1d61b0b6925a443a6e51c2e764",
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

response = requests.post(create_url, headers=header, json=task)

if response.status_code == 201:
    print(f"Task successfully created. Content: {response.json()}")
else:
    print(f"Error creating task. Status code: {response.status_code}. Error: {response.json()}")
