"""
Streamlit Test App for LangChain Greeter + Weather Agent
Test the agent deployed in Podman container
"""
import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LangChain Agent Tester",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background-color: #f1f8e9;
        border-left: 4px solid #8bc34a;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .step-message {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🤖 LangChain Agent Tester</h1>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_url = st.text_input(
        "Agent API URL",
        value="http://localhost:5001/chat",
        help="URL of the deployed LangChain agent"
    )
    
    use_streaming = st.checkbox(
        "Enable Streaming",
        value=True,
        help="Use Server-Sent Events for streaming responses"
    )
    
    show_cot = st.checkbox(
        "Show Chain of Thought",
        value=True,
        help="Display intermediate reasoning steps"
    )
    
    st.divider()
    
    # Test connection
    if st.button("🔍 Test Connection"):
        try:
            health_url = api_url.replace("/chat", "/health")
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                st.success("✅ Agent is online!")
                st.json(response.json())
            else:
                st.error(f"❌ Agent returned status {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
    
    st.divider()
    
    # Example prompts
    st.subheader("📝 Example Prompts")
    example_prompts = [
        "My name is John and I'm in New York",
        "Hi, I'm Sarah from San Francisco",
        "I'm Mike in Chicago, what's the weather like?",
        "My name is Alice and I'm in Boston"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=f"example_{prompt}"):
            st.session_state.user_input = prompt

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main chat interface
st.subheader("💬 Chat with the Agent")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>',
            unsafe_allow_html=True
        )
    elif message["role"] == "agent":
        st.markdown(
            f'<div class="chat-message agent-message"><strong>Agent:</strong> {message["content"]}</div>',
            unsafe_allow_html=True
        )
    elif message["role"] == "step" and show_cot:
        st.markdown(
            f'<div class="chat-message step-message"><strong>Step:</strong> {message["content"]}</div>',
            unsafe_allow_html=True
        )
    elif message["role"] == "error":
        st.markdown(
            f'<div class="chat-message error-message"><strong>Error:</strong> {message["content"]}</div>',
            unsafe_allow_html=True
        )

# Chat input
user_input = st.text_input(
    "Your message:",
    key="user_input",
    placeholder="Type your message here... (e.g., 'My name is John and I'm in New York')"
)

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    send_button = st.button("📤 Send", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear Chat", use_container_width=True)

if clear_button:
    st.session_state.messages = []
    st.rerun()

# Send message
if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Prepare request
    payload = {
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "stream": use_streaming
    }
    
    try:
        with st.spinner("🤔 Agent is thinking..."):
            if use_streaming:
                # Streaming request
                response = requests.post(
                    api_url,
                    json=payload,
                    stream=True,
                    timeout=30
                )
                
                if response.status_code == 200:
                    agent_response = ""
                    steps = []
                    
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                data = json.loads(line[6:])
                                
                                if data.get('type') == 'step':
                                    step_info = f"Tool: {data.get('action')} | Input: {data.get('input')} | Output: {data.get('output')}"
                                    steps.append(step_info)
                                    if show_cot:
                                        st.session_state.messages.append({
                                            "role": "step",
                                            "content": step_info,
                                            "timestamp": datetime.now().isoformat()
                                        })
                                
                                elif data.get('type') == 'response':
                                    agent_response = data.get('content', '')
                                
                                elif data.get('type') == 'error':
                                    st.session_state.messages.append({
                                        "role": "error",
                                        "content": data.get('message', 'Unknown error'),
                                        "timestamp": datetime.now().isoformat()
                                    })
                    
                    if agent_response:
                        st.session_state.messages.append({
                            "role": "agent",
                            "content": agent_response,
                            "timestamp": datetime.now().isoformat()
                        })
                else:
                    st.session_state.messages.append({
                        "role": "error",
                        "content": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": datetime.now().isoformat()
                    })
            
            else:
                # Non-streaming request
                response = requests.post(
                    api_url,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Add intermediate steps if available
                    if show_cot and 'intermediate_steps' in data:
                        for step in data['intermediate_steps']:
                            step_info = f"Tool: {step.get('tool')} | Input: {step.get('input')} | Output: {step.get('output')}"
                            st.session_state.messages.append({
                                "role": "step",
                                "content": step_info,
                                "timestamp": datetime.now().isoformat()
                            })
                    
                    # Add agent response
                    st.session_state.messages.append({
                        "role": "agent",
                        "content": data.get('response', 'No response'),
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    st.session_state.messages.append({
                        "role": "error",
                        "content": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": datetime.now().isoformat()
                    })
        
        st.rerun()
    
    except Exception as e:
        st.session_state.messages.append({
            "role": "error",
            "content": f"Request failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🤖 LangChain Greeter + Weather Agent Tester</p>
    <p>Powered by OpenAI GPT-4o-mini | Made with Bob</p>
</div>
""", unsafe_allow_html=True)
