# path('auth/', obtain_auth_token),
# path('task/<int:pk>', TaskDetailAPIView.as_view(), name='task_detail'),
# path('task/create/', TaskCreateAPIView.as_view(), name='task_create'),
# path('task/update/<int:pk>', TaskUpdateAPIView.as_view(), name='task_update'),
# path('task/disable/<int:pk>', TaskDisableAPIView.as_view(), name='task_disable'),
# path('task/', TaskListAPIView.as_view(), name='task_list'),

import requests
from getpass import getpass

auth_to_use = input('What auth to use?\n(Press "T" for token or "P" for Password:')

if auth_to_use == "T":
    token = '2fcdfbad5ce716cc1d5e969373bc1fbadb6d1b5d'
    headers = {
        "Authorization": f"Token {token}",
    }

else:
    auth_endpoint = "http://127.0.0.1:8000/api/auth/"
    username = input ("What is your username?\n")
    password = getpass ("What is your password?\n")
    auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password})

    if auth_response.status_code == 200:
        token = auth_response.json()['token']
        print(token)
        headers = {
            "Authorization": f"Token {token}"
        }

endpoint = "http://localhost:8000/api/task/create/"

payload = {
    "name": "Task from API",
    "done": False,
}

# Build the request
req = requests.Request("POST", endpoint, json=payload, headers=headers)
prepared_req = req.prepare()

# You can print the whole request here
print(prepared_req.url)
print(prepared_req.method)
print(prepared_req.headers)
print(prepared_req.body)

# Send the request
response = requests.Session().send(prepared_req)

if response.status_code == 200:
    print(response.json())
else:
    print("Request failed")
