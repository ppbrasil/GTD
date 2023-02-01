import requests

# endpoint = "http://httpbin.org/status/200"
task_id = 1
endpoint = "http://localhost:8000/api/{}/".format(task_id)

response = requests.get(endpoint)
    
print(response.text)
# print(get_response.status_code)
# print(get_response.json())


