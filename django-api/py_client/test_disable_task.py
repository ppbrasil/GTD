import requests
import json

task_id = input("Enter the task id: ")
retrieve_url = f"http://localhost:8000/api/task/{task_id}/"
toggle_focus_url = f"http://localhost:8000/api/task/disable/{task_id}/"
header = {
    "Authorization": "Token fe96bd6bcd97aaa9d6ecb1570db672490325ddc4",
    "Content-Type": "application/json"
}

# Retrieve task information
response = requests.get(retrieve_url, headers=header)

if response.status_code == 200:
    task = response.json()
    print("Current task information:")
    print(json.dumps(task, indent=4))

    # Toggle disbale of task
    response = requests.patch(toggle_focus_url, headers=header)

    if response.status_code == 200:
        task = response.json()
        print("Task successfully disabled:")
        print(json.dumps(task, indent=4))
    else:
        print(f"Error toggling focus. Status code: {response.status_code}. Error: {response.json()}")
else:
    print(f"Error retrieving task. Status code: {response.status_code}. Error: {response.json()}")
