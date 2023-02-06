import requests

url = 'http://localhost:8000/api/auth/logout/'

header = {
    "Authorization": "Token fe96bd6bcd97aaa9d6ecb1570db672490325ddc4",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=header)

print(response.status_code)
print(response.text)