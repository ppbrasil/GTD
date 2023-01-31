import requests

# endpoint = "http://httpbin.org/status/200"
endpoint = "http://localhost:8000/api/"

get_response = requests.get(endpoint, params={
    
})

print(get_response.text)
# print(get_response.status_code)
# print(get_response.json())


