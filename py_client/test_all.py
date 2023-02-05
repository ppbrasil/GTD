import requests
import json

# Get authentication token
response = requests.post("http://localhost:8000/api/auth/", data={"username": "pedro", "password": "Q!w2e3r4T%"})
token = response.json()["token"]

headers = {
    "Authorization": "Token " + token,
    "Content-Type": "application/json"
}

# Call TaskDetailAPIView
task_id = 1
response = requests.get(f"http://localhost:8000/api/task/{task_id}/", headers=headers)
print("Task detail:", response.json())

# Call TaskCreateAPIView
task_data = {"title": "Test task", "description": "Test task description"}
response = requests.post("http://localhost:8000/api/task/create/", headers=headers, data=json.dumps(task_data))
print("Task created:", response.json())

# Call TaskUpdateAPIView
task_id = 2
task_data = {"title": "Updated task", "description": "Updated task description"}
response = requests.put(f"http://localhost:8000/api/task/update/{task_id}/", headers=headers, data=json.dumps(task_data))
print("Task updated:", response.json())

# Call TaskToggleFocusAPIView
task_id = 2
previous_task = requests.get(f"http://localhost:8000/api/task/{task_id}/", headers=headers).json()
print("Task before toggle focus:", previous_task)
response = requests.put(f"http://localhost:8000/api/task/toggle-focus/{task_id}/", headers=headers)
print("Task after toggle focus:", response.json())

# Call TaskToggleDoneAPIView
task_id = 2
previous_task = requests.get(f"http://localhost:8000/api/task/{task_id}/", headers=headers).json()
print("Task before toggle done:", previous_task)
response = requests.put(f"http://localhost:8000/api/task/toggle-done/{task_id}/", headers=headers)
print("Task after toggle done:", response.json())

# Call TaskListFocusedAPIView
response = requests.get("http://localhost:8000/api/task/focused/", headers=headers)
print("Focused task list:", response.json())

# Call TaskListDoneAPIView
response = requests.get("http://localhost:8000/api/task/done/", headers=headers)
print("Done task list:", response.json())

# Call TaskListReadinessInboxAPIView
response = requests.get("http://localhost:8000/api/task/inbox/", headers=headers)
print("Inbox task list:", response.json())

# Call TaskListReadinessSometimeAPIView
response = requests.get("http://localhost:8000/api/task/sometime/", headers=headers)
print("Sometime task list:", response.json())

# Call TaskListReadinessAnytimeAPIView
response = requests.get("http://localhost:8000/api/task/anytime/", headers=headers)
print("Anytime task list:", response.json())