# path('auth/', obtain_auth_token),
# path('task/<int:pk>', TaskDetailAPIView.as_view(), name='task_detail'),
# path('task/create/', TaskCreateAPIView.as_view(), name='task_create'),
# path('task/update/<int:pk>', TaskUpdateAPIView.as_view(), name='task_update'),
# path('task/disable/<int:pk>', TaskDisableAPIView.as_view(), name='task_disable'),
# path('task/', TaskListAPIView.as_view(), name='task_list'),

import requests
from getpass import getpass

auth_endpoint = "http://localhost:8000/api/auth/"
username = input ("What is your username?\n")
password = input ("What is your password?\n")

auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password})

print (auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://localhost:8000/api/task/"

    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())