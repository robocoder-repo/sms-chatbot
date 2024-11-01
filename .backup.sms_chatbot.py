
import gradio as gr
import requests

API_BASE_URL = 'https://api.httpsms.com/v1'
API_KEY = 'VmM2kyFx0XGRklix4TnXb9GloZx-TQRPt82PdQ-9bKjAmJIdHXH4kr6HiKqvZSdS'

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

def chatbot(from_number, to_number, message):
    # Store the message in conversation history
    if from_number not in conversations:
        conversations[from_number] = []
    conversations[from_number].append({"from": from_number, "content": message})
    
    # Generate and send response
    response = generate_response(message)
    send_result = send_sms(to_number, from_number, response)
    
    # Return both the chatbot's response and the SMS sending result
    return response, str(send_result)

iface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.Textbox(label="From Number"),
        gr.Textbox(label="To Number"),
        gr.Textbox(label="Message")
    ],
    outputs=[
        gr.Textbox(label="Chatbot Response"),
        gr.Textbox(label="SMS Sending Result")
    ],
    title="SMS Chatbot",
    description="Enter the 'from' number, 'to' number, and your message to interact with the SMS chatbot."
)

iface.launch()
