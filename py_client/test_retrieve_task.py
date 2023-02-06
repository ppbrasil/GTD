import requests

task_id = input("Enter the task id: ")

url = f"http://localhost:8000/api/task/{task_id}/"
header = {
    "Authorization": "Token 84c734198cd0e413707943cada118abe22840ddf",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=header)

if response.status_code == 200:
    print(f"Task successfully retrieved. Content: {response.json()}")
else:
    print(f"Error retrieving task. Status code: {response.status_code}. Error: {response.json()}")
