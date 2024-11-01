
import requests

API_BASE_URL = 'https://api.httpsms.com/v1'
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with actual API key when available

def send_sms(from_number, to_number, content):
    url = f"{API_BASE_URL}/messages/send"
    headers = {
        'x-api-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "from": from_number,
        "to": to_number,
        "content": content
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Test the send_sms function
if __name__ == "__main__":
    result = send_sms("+18005550199", "+18005550100", "Hello, this is a test message!")
    print(result)
