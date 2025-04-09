import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Open WebUI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Open WebUI API configuration
OPENWEBUI_API_URL = os.getenv("OPENWEBUI_API_URL", "http://localhost:8080")
API_KEY = os.getenv("OPENWEBUI_API_KEY", "")

def send_message(message):
    """Send message to Open WebUI API and get response"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(
            f"{OPENWEBUI_API_URL}/api/chat",
            headers=headers,
            json={"message": message}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar for configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_url = st.text_input("Open WebUI API URL", value=OPENWEBUI_API_URL)
    api_key = st.text_input("API Key", value=API_KEY, type="password")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("💬 Open WebUI Chatbot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_message(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response}) 