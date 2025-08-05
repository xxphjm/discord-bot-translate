import requests
import json
import os

# Test the webhook with a sample message
webhook_url = 'https://hook.eu2.make.com/woprpcgkuw7degky8vovtmz1tdznwtf0'
api_key= os.environ.get("WEBHOOK_API_KEY", "NA")

test_data = {
    'text': 'Hello, how are you?'
}

headers = {
    'x-make-apikey': api_key,
    'Content-Type': 'application/json'
}

try:
    response = requests.post(webhook_url, json=test_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            print(f"JSON Response: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
        except ValueError:
            print("Response is not valid JSON")
    else:
        print(f"HTTP Error: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

