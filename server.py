from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import json

app = Flask(__name__)

# Configure CORS properly to handle preflight requests
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": "*"}})

# Initialize Bedrock Runtime client
bedrock = boto3.client('bedrock-runtime')

def generate_response(context):
    try:
        input_data = {
            "messages": context
        }

        response = bedrock.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            body=json.dumps(input_data),
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = response['body'].read().decode('utf-8')
        response_data = json.loads(response_body)
        content_list = response_data.get('output', {}).get('message', {}).get('content', [])
        formatted_response = "\n".join([item.get('text', '') for item in content_list])
        return formatted_response.strip() if formatted_response else "No response from model."
        
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    context = data.get('context', [])
    response = generate_response(context)
    return jsonify({"response": response})

# Add a route for handling OPTIONS requests
@app.route('/chat', methods=['OPTIONS'])
def handle_options():
    return '', 200

def main():
    app.run(port=5050, debug=True)

if __name__ == "__main__":
    main()