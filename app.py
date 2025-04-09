import streamlit as st
import requests
import os
from dotenv import load_dotenv
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Open WebUI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Open WebUI API configuration
OPENWEBUI_API_URL = os.getenv("OPENWEBUI_API_URL", "http://localhost:8080")
API_KEY = os.getenv("OPENWEBUI_API_KEY", "")

def get_available_models():
    """Fetch available models from Open WebUI"""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        response = requests.get(
            f"{OPENWEBUI_API_URL}/api/models",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching models: {str(e)}")
        return []

def send_message(message, model):
    """Send message to Open WebUI API chat completions endpoint"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{OPENWEBUI_API_URL}/api/chat/completions",
            headers=headers,
            json=payload,
            verify=False
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar for configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_url = st.text_input("Open WebUI API URL", value=OPENWEBUI_API_URL)
    api_key = st.text_input("API Key", value=API_KEY, type="password")
    
    # Model selection
    st.subheader("🤖 Model Selection")
    models = get_available_models()
    if models:
        model_names = [model.get("name", model.get("id")) for model in models]
        selected_model = st.selectbox(
            "Choose a model",
            options=model_names,
            index=0 if model_names else None
        )
        if selected_model:
            st.session_state.selected_model = selected_model
    else:
        st.error("No models available. Please check your API configuration.")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("💬 Open WebUI Chatbot")

if not st.session_state.selected_model:
    st.warning("Please select a model in the sidebar to start chatting.")
else:
    st.info(f"Using model: {st.session_state.selected_model}")
    
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
                response = send_message(prompt, st.session_state.selected_model)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response}) 