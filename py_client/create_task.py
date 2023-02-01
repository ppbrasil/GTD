import requests
from django.contrib.auth.models import User

user = User.objects.get(pk=1)

url = "http://localhost:8000/api/task/create/"

payload = {
    "user": user.id,
    "name": "Task from API",
    "done": False,
}

response = requests.post(url, json=payload)
    
# print(get_response.status_code)
# print(get_response.json())

if response.status_code == 200:
    print(response.json())
else:
    print("Request failed")
