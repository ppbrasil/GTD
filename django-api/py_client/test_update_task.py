import requests
import json

task_id = input("Enter the task id: ")
retrieve_url = f"http://localhost:8000/api/task/{task_id}/"
update_url = f"http://localhost:8000/api/task/update/{task_id}/"
header = {
    "Authorization": "Token 861a2a0d21b6d62e88263b2e238b671f47cf4e1f",
    "Content-Type": "application/json"
}

response = requests.get(retrieve_url, headers=header)

if response.status_code == 200:
    task = response.json()
    print("Current task information:")
    print(json.dumps(task, indent=4))

    task["name"] = input("Enter a new name: ")
    task["notes"] = input("Enter new notes: ")

    response = requests.patch(update_url, headers=header, json=task)
    print("Request URL: ", response.url)
    print("Request Headers: ", response.request.headers)
    print("Request Body: ", response.request.body)


    if response.status_code == 200:
        task = response.json()
        print("Task successfully updated:")
        print(json.dumps(task, indent=4))
    else:
        print(f"Error updating task. Status code: {response.status_code}. Error: {response.json()}")
else:
    print(f"Error retrieving task. Status code: {response.status_code}. Error: {response.json()}")

