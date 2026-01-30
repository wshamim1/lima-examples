"""
Flask API for LangChain Greeter + Weather Agent
Exposes the agent as an external API for IBM WatsonX Orchestrate
"""
import os
import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
from greeter_weather_agent import create_greeter_agent
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Authentication token (optional)
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", None)

# Initialize agent
agent_executor = None

def get_agent():
    """Get or create agent executor"""
    global agent_executor
    if agent_executor is None:
        agent_executor = create_greeter_agent()
    return agent_executor

def verify_auth(request):
    """Verify authentication token (optional)"""
    # If no AUTH_TOKEN is set, skip authentication
    if AUTH_TOKEN is None:
        return True
    
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header:
        return False
    
    # Support both "Bearer <token>" and "<token>" formats
    token = auth_header.replace("Bearer ", "").strip()
    return token == AUTH_TOKEN

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "langchain-greeter-weather-agent"
    })

@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for WatsonX Orchestrate external agent
    
    Expected request format:
    {
        "messages": [
            {"role": "user", "content": "My name is John and I'm in New York"}
        ],
        "stream": true/false
    }
    """
    # Verify authentication (optional)
    if not verify_auth(request):
        return jsonify({"error": "Unauthorized - No authentication required if API_AUTH_TOKEN is not set"}), 401
    
    try:
        data = request.get_json()
        
        if not data or "messages" not in data:
            return jsonify({"error": "Invalid request format"}), 400
        
        messages = data.get("messages", [])
        stream = data.get("stream", False)
        
        # Get the last user message
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content")
                break
        
        if not user_message:
            return jsonify({"error": "No user message found"}), 400
        
        logger.info(f"Processing request: {user_message}")
        
        # Get agent
        agent = get_agent()
        
        if stream:
            # Streaming response
            return Response(
                stream_response(agent, user_message),
                mimetype="text/event-stream"
            )
        else:
            # Non-streaming response
            result = agent.invoke({"input": user_message})
            response = {
                "response": result.get("output", ""),
                "intermediate_steps": format_intermediate_steps(result)
            }
            return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

def stream_response(agent, user_input):
    """Stream agent response using Server-Sent Events (SSE)"""
    try:
        # For streaming, we'll send the response in chunks
        result = agent.invoke({"input": user_input})
        
        # Send intermediate steps if available
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                action, observation = step
                event_data = {
                    "type": "step",
                    "action": str(action.tool),
                    "input": str(action.tool_input),
                    "output": str(observation)
                }
                yield f"data: {json.dumps(event_data)}\n\n"
        
        # Send final response
        final_data = {
            "type": "response",
            "content": result.get("output", "")
        }
        yield f"data: {json.dumps(final_data)}\n\n"
        
        # Send done signal
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
    except Exception as e:
        error_data = {
            "type": "error",
            "message": str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"

def format_intermediate_steps(result):
    """Format intermediate steps for response"""
    steps = []
    if "intermediate_steps" in result:
        for step in result["intermediate_steps"]:
            action, observation = step
            steps.append({
                "tool": str(action.tool),
                "input": str(action.tool_input),
                "output": str(observation)
            })
    return steps

@app.route("/", methods=["GET"])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "service": "LangChain Greeter + Weather Agent",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)"
        },
        "description": "External agent API for IBM WatsonX Orchestrate"
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)

