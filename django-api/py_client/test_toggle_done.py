import requests
import json

task_id = input("Enter the task id: ")
retrieve_url = f"http://localhost:8000/api/task/{task_id}/"
toggle_focus_url = f"http://localhost:8000/api/task/toggle-done/{task_id}/"
header = {
    "Authorization": "Token 861a2a0d21b6d62e88263b2e238b671f47cf4e1f",
    "Content-Type": "application/json"
}

# Retrieve task information
response = requests.patch(toggle_focus_url, headers=header)

if response.status_code == 200:
    if response.content:
        task = response.json()
        print("Task successfully toggled done:")
        print(json.dumps(task, indent=4))
    else:
        print("Task successfully toggled done.")
else:
    print(f"Error toggling focus. Status code: {response.status_code}. Error: {response.json()}")
