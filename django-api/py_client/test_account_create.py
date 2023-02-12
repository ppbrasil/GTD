import requests

url = 'http://localhost:8000/api/account/create/'

username = input('Enter username: ')
password = input('Enter password: ')
email = input('Enter email: ')

data = {
    'username': username,
    'password': password,
    'email': email,
    'is_active': True
}

req = requests.Request("POST", url, json=data)
prepared_req = req.prepare()

print(prepared_req.url)
print(prepared_req.method)
print(prepared_req.headers)
print(prepared_req.body)

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)