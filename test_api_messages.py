import requests

# URL of the deployed application
url = "https://ai-master-item-agent.onrender.com/api/messages"

# Sample payload mimicking a Microsoft Teams message
payload = {
    "type": "message",
    "text": "Hello, AI Agent!",
    "from": {
        "id": "user1",
        "name": "Test User"
    },
    "recipient": {
        "id": "bot",
        "name": "MasterItemBot"
    },
    "conversation": {
        "id": "conversation1"
    },
    "service_url": "https://smba.trafficmanager.net/emea/",
    "channelId": "msteams",
    "locale": "en-US",
    "timestamp": "2025-08-28T12:00:00Z"
}

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer VALID_TOKEN"  # Replace VALID_TOKEN with an actual token
}

# Send POST request
response = requests.post(url, json=payload, headers=headers)

# Print response
print("Status Code:", response.status_code)
print("Response Body:", response.text)
