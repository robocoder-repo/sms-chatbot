
import requests
from flask import Flask, request, jsonify

API_BASE_URL = 'https://api.httpsms.com/v1'
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with actual API key when available

app = Flask(__name__)

# In-memory storage for conversation history
conversations = {}

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

def get_message_history(owner, contact):
    url = f"{API_BASE_URL}/messages"
    headers = {
        'x-api-Key': API_KEY
    }
    params = {
        "owner": owner,
        "contact": contact,
        "limit": 20  # Adjust as needed
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def generate_response(message):
    # Simple response logic - can be expanded later
    return f"You said: {message}. How can I help you?"

@app.route('/receive_sms', methods=['POST'])
def receive_sms():
    data = request.json
    from_number = data['from']
    to_number = data['to']
    content = data['content']
    
    # Store the message in conversation history
    if from_number not in conversations:
        conversations[from_number] = []
    conversations[from_number].append({"from": from_number, "content": content})
    
    # Generate and send response
    response = generate_response(content)
    send_sms(to_number, from_number, response)
    
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
