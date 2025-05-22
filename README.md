# Foundations Of Natural Language AI

## API Overview

This chat application uses a single endpoint to interact with AWS Bedrock. This endpoint handles context-based conversational AI requests and has memory up to the previous 10 messages.

- Base URL: http://localhost:5050
- Content Type: application/json

Endpoint: /chat

- Method: POST
- Sends a user message along with previous conversation context to generate a response from the AI model.

Request Body Structure:
- context: An array of message objects representing the current conversation context.

Message Object Structure:
- role: "user" or "assistant"
- content: An array of content objects, each containing a text field.

Content Object Structure:
- text: The text content of the message.

Request Example:

```json
{
  "context": [
    {
      "role": "user",
      "content": [{ "text": "What is the weather like today?" }]
    },
    {
      "role": "assistant",
      "content": [{ "text": "I'm not sure. Would you like me to check?" }]
    },
    {
      "role": "user",
      "content": [{ "text": "Yes, please." }]
    }
  ]
}
```

Response Structure:
- response: A string containing the AI-generated response.

```json
{
  "response": "The current weather is sunny with a temperature of 75°F."
}
```

Error Handling
- If the request is malformed or if the AI model fails to generate a response, the server returns a structured error message

```json
{
  "response": "Unable to connect to the server. Please try again."
}
```

## Technical Documentation

### Frontend Overview:

The frontend of this application is a React application designed chatbot where users can input messages and receive AI-generated responses. It maintains conversation context and each message is categorized as either a user message, assistant response, or error notification. Axios handles communication with the backend, while ReactMarkdown is used for rendering AI responses with structured formatting.

### Backend Overview:

The backend is implemented using Flask and is essentially the middle-man between the frontend and Amazon Bedrock. It exposes a /chat endpoint that accepts context data, processes it through AWS Bedrock, and returns the AI's response. The backend also handles error responses, memory management and ensures the format of the input and output data aligns with expected specifications.

### Installation & Setup

#### Backend:

1. Navigate to the backend directory:
```
cd backend
```
2. Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Start the server:
```
python server.py
```
5. (Optional) If you want to run tests:
```
python test_server.py
```
* Note: To run tests for the backend, the backend must be running otherwise they will fail as we are testing the endpoints

#### Frontend:

1. Navigate to the frontend directory:
```
cd frontend
```
2. Install dependencies:
```
npm install
```
3. Start the development server:
```
npm start
```
4. (Optional) If you want to run tests:
```
npm test
```

### Key Components & Functions

#### Backend (server.py):

- generate_response(context) - Handles interaction with Bedrock and processes the response.
- /chat endpoint - Receives context and returns AI response.

#### Frontend (App.jsx):

- handleSend() - Processes user input, sends it to the server, and manages context.
- useEffect() - Scrolls to the latest message on each render.
- Error Handling: Catches Axios errors and displays them as chat messages.

### Error Handling

- Network Errors: Displays a user-friendly error message when the backend is unreachable.
- Response Structure Validation: Ensures that API responses contain a valid structure before rendering.
- Error Logging: Logs error messages to the console for debugging.

### Testing Strategy

* **Frontend:**
  * Tests for rendering components and handling API errors.
  * Verifies state updates and context management.

* **Backend:**

  * Tests endpoint responses and error handling.
  * Validates response structure and error message format.