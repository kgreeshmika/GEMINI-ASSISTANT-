# Gemini Work Assistant

## Overview

Gemini Work Assistant is a Flask-based AI assistant developed using the Google Gemini API. The application provides conversational assistance while maintaining conversation history across messages.

The application also supports real-time web and news searches using DDGS. For current or time-sensitive questions, the assistant can search the web or recent news and provide the retrieved information along with source links.

This project was developed as part of the QSkill Python Development Internship.


## Features

- AI-powered conversational assistant using Google Gemini API
- Maintains conversation history during a session
- Remembers previous user and assistant messages
- Real-time web search for current information
- Real-time news search for recent events
- Displays source links for searched information
- Clear conversation functionality
- Empty-input validation
- API error handling
- Retry mechanism for temporary Gemini service errors
- Flask-based web interface
- Environment-variable based API key configuration


## Technologies Used

- Python
- Flask
- Google Gemini API
- Google GenAI Python SDK
- DDGS
- HTML
- CSS
- python-dotenv


## Project Structure

```text
GEMINI_ASSISSTANT/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## How It Works

The application is built using Flask and communicates with the Google Gemini API through the Google GenAI Python SDK.

When a user sends a message:

1. The message is received by the Flask `/chat` endpoint.
2. The message is added to the conversation history.
3. Gemini processes the conversation.
4. For current or time-sensitive questions, Gemini can use the available search tools.
5. The search tools retrieve relevant web or news results using DDGS.
6. Gemini uses the retrieved information to generate a response.
7. Source links are returned to the frontend and displayed below the response.
8. Gemini's response is added to the conversation history.


## Conversation History

The application maintains conversation history using a Python list during the current application session.

Both user messages and Gemini responses are stored during the current application session. This allows the assistant to use previous messages as context for later questions.

For example:

User: My name is Greeshmika.

Assistant: Nice to meet you, Greeshmika!

User: What is my name?

Assistant: Your name is Greeshmika.

The conversation can be cleared using the **Clear Conversation** option.

After clearing the conversation, previously stored messages are removed and the assistant no longer has access to that conversation history.


## Real-Time Search

The application provides two search functions:

### Web Search

The `web_search` function is used for general current information such as:

- Latest software versions
- Current facts
- Documentation
- Prices
- Other time-sensitive information

Example:
What is the latest version of Python?

### News Search

The `news_search` function is used for recent news and current events.

Example:
What are the latest technology news today?

When a search is performed, the application collects the URLs returned by the search tool and displays them as source links in the interface.

> **Note:** Real-time web and news search in this project is implemented using DDGS. The project does not claim to use Google's built-in Gemini Search grounding or Google Custom Search API.


## Environment Setup

### 1. Create a Virtual Environment

Open a terminal in the project directory and run:
python -m venv venv

### 2. Activate the Virtual Environment

#### Windows PowerShell

.\venv\Scripts\Activate.ps1

If PowerShell blocks script execution for the current terminal session, use:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1


### 3. Install Dependencies

pip install -r requirements.txt


## API Key Configuration

Create a `.env` file in the project root directory:

GEMINI_API_KEY=your_gemini_api_key_here

The API key is loaded using `python-dotenv`.

## Running the Application

After activating the virtual environment and configuring the API key, run:
python app.py

The Flask development server will start locally.

Open the application in a browser at:
[http://127.0.0.1:5000]

## Example Queries

### General Question

What is Python?

### Conversation Memory

First message:

My name is Greeshmika.

Followed by:

What is my name?

### Web Search

What is the latest version of Python?

### News Search

What are the latest technology news today?

## Error Handling

The application includes handling for:

- Empty user messages
- Missing Gemini API key
- Gemini API quota errors
- Temporary Gemini service errors
- Search tool failures
- Empty Gemini responses

Temporary service errors are retried before returning an error message to the user.

The application also removes the user's latest message from the conversation history when a request fails, preventing an unsuccessful request from remaining as an incomplete conversation turn.

## Security

The Gemini API key is stored in an environment variable instead of being written directly into the Python source code.

The `.env.example` file contains only a placeholder and does not contain the actual API key.

## Internship Task

This project was developed as one of the selected tasks for the **QSkill Python Development Internship** under the **Python Development** domain.

The project demonstrates:

- Python development
- Flask web application development
- Google Gemini API integration
- Conversation history
- Function/tool-based web and news search
- Real-time information retrieval
- Error handling
- Environment-variable configuration

## Author

**Kondabathula Greeshmika**