# Open WebUI Chatbot

A Streamlit-based chatbot that interfaces with Open WebUI.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Open WebUI configuration:

```
OPENWEBUI_API_URL=http://your-openwebui-url:port
OPENWEBUI_API_KEY=your-api-key
```

## Running the Application

To run the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## Features

- Clean and modern chat interface
- Configurable Open WebUI API URL and API key
- Chat history persistence during the session
- Clear chat history option
- Error handling for API communication

## Configuration

You can configure the following settings in the sidebar:

- Open WebUI API URL
- API Key
- Clear chat history
