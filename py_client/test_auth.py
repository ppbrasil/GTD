import requests

# make a POST request to the `/auth/` endpoint to obtain the authentication token
response = requests.post('http://localhost:8000/api/auth/', data={
    'username': 'pedro',
    'password': 'Q!w2e3r4T%',
})

# check if the request was successful
if response.status_code == 200:
    # retrieve the token from the response
    token = response.json()['token']
    print(f'Authentication token: {token}')
else:
    print(f'Failed to obtain authentication token: {response.content}')
