import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add the root directory to sys.path to import server
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from server import app, generate_response

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chat_endpoint_valid_context(client):
    payload = {
        "context": [
            {"role": "user", "content": [{"text": "What is the capital of France?"}]}
        ]
    }
    response = client.post('/chat', 
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "response" in data

def test_chat_endpoint_empty_context(client):
    payload = {"context": []}
    response = client.post('/chat', 
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "response" in data

def test_chat_endpoint_no_context(client):
    payload = {}
    response = client.post('/chat', 
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "response" in data

def test_chat_endpoint_invalid_json(client):
    response = client.post('/chat', 
                          data='invalid json',
                          content_type='application/json')
    assert response.status_code == 400

def test_options_endpoint(client):
    response = client.options('/chat')
    assert response.status_code == 200

@patch('server.bedrock')
def test_generate_response_success(mock_bedrock):
    mock_response = {
        'body': MagicMock()
    }
    mock_response['body'].read.return_value = json.dumps({
        'output': {
            'message': {
                'content': [
                    {'text': 'Paris is the capital of France.'}
                ]
            }
        }
    }).encode('utf-8')
    
    mock_bedrock.invoke_model.return_value = mock_response
    
    context = [{"role": "user", "content": [{"text": "What is the capital of France?"}]}]
    result = generate_response(context)
    
    assert result == "Paris is the capital of France."
    mock_bedrock.invoke_model.assert_called_once()

@patch('server.bedrock')
def test_generate_response_multiple_content(mock_bedrock):
    mock_response = {
        'body': MagicMock()
    }
    mock_response['body'].read.return_value = json.dumps({
        'output': {
            'message': {
                'content': [
                    {'text': 'First part.'},
                    {'text': 'Second part.'}
                ]
            }
        }
    }).encode('utf-8')
    
    mock_bedrock.invoke_model.return_value = mock_response
    
    context = [{"role": "user", "content": [{"text": "Tell me something"}]}]
    result = generate_response(context)
    
    assert result == "First part.\nSecond part."

@patch('server.bedrock')
def test_generate_response_empty_content(mock_bedrock):
    mock_response = {
        'body': MagicMock()
    }
    mock_response['body'].read.return_value = json.dumps({
        'output': {
            'message': {
                'content': []
            }
        }
    }).encode('utf-8')
    
    mock_bedrock.invoke_model.return_value = mock_response
    
    context = [{"role": "user", "content": [{"text": "Test"}]}]
    result = generate_response(context)
    
    assert result == "No response from model."

@patch('server.bedrock')
def test_generate_response_no_output(mock_bedrock):
    mock_response = {
        'body': MagicMock()
    }
    mock_response['body'].read.return_value = json.dumps({}).encode('utf-8')
    
    mock_bedrock.invoke_model.return_value = mock_response
    
    context = [{"role": "user", "content": [{"text": "Test"}]}]
    result = generate_response(context)
    
    assert result == "No response from model."

@patch('server.bedrock')
def test_generate_response_exception(mock_bedrock):
    mock_bedrock.invoke_model.side_effect = Exception("AWS Error")
    
    context = [{"role": "user", "content": [{"text": "Test"}]}]
    result = generate_response(context)
    
    assert "Error: AWS Error" in result

@patch('server.bedrock')
def test_generate_response_json_decode_error(mock_bedrock):
    mock_response = {
        'body': MagicMock()
    }
    mock_response['body'].read.return_value = b'invalid json'
    
    mock_bedrock.invoke_model.return_value = mock_response
    
    context = [{"role": "user", "content": [{"text": "Test"}]}]
    result = generate_response(context)
    
    assert "Error:" in result

def test_chat_endpoint_integration(client):
    with patch('server.bedrock') as mock_bedrock:
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'output': {
                'message': {
                    'content': [
                        {'text': 'Integration test response'}
                    ]
                }
            }
        }).encode('utf-8')
        
        mock_bedrock.invoke_model.return_value = mock_response
        
        payload = {
            "context": [
                {"role": "user", "content": [{"text": "Integration test"}]}
            ]
        }
        response = client.post('/chat', 
                              data=json.dumps(payload),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["response"] == "Integration test response"