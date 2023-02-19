import requests

task_id = input("Enter the task id: ")

url = f"http://localhost:8000/api/task/{task_id}/"
header = {
    "Authorization": "Token 861a2a0d21b6d62e88263b2e238b671f47cf4e1f",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=header)

if response.status_code == 200:
    print(f"Task successfully retrieved. Content: {response.json()}")
else:
    print(f"Error retrieving task. Status code: {response.status_code}. Error: {response.json()}")
