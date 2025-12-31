import requests

url = "http://localhost:8000/chat"
payload = {
    "message": "Artificial Intelligence will replace human jobs."
}

response = requests.post(url, json=payload)
print(response.json()["reply"])