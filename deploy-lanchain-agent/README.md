# LangChain Greeter + Weather Agent

A production-ready LangChain agent powered by OpenAI that combines greeting and weather functionality. Deploy with Docker/Podman and test with Streamlit.

## 🚀 Quick Start

**Get running in 5 minutes:**

```bash
# 1. Configure environment
echo "OPENAI_API_KEY=sk-your-key-here" > ../.env

# 2. Deploy with Podman
cd langchain-agents
./deploy_podman.sh deploy

# 3. Test with Streamlit
./run_streamlit.sh
```

**Access:** http://localhost:8501

📖 **[Complete Quick Start Guide →](QUICKSTART.md)**

## Overview

This agent demonstrates a complete LangChain deployment pipeline:
1. **Greets users** by name
2. **Fetches weather** information for their city
3. **Combines both** into a personalized welcome message
4. **Deploys as API** in Docker/Podman container
5. **Tests with Streamlit** interactive interface


## Architecture

```
┌─────────────────────────────────────┐
│   Streamlit App (Port 8501)         │
│   - User Interface                  │
│   - Test Controls                   │
└──────────────┬──────────────────────┘
               │ HTTP Requests
               ↓
┌─────────────────────────────────────┐
│   Docker/Podman Container           │
│   ┌───────────────────────────────┐ │
│   │  Flask API (Port 5000→5001)   │ │
│   │  - /health                    │ │
│   │  - /chat (streaming/non)      │ │
│   └─────────────┬─────────────────┘ │
│                 ↓                   │
│   ┌───────────────────────────────┐ │
│   │  LangChain Agent (ReAct)      │ │
│   │  - OpenAI GPT-4o-mini         │ │
│   │  - Weather Tools              │ │
│   │  - Greeter Tools              │ │
│   └───────────────────────────────┘ │
└─────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   OpenAI API                        │
└─────────────────────────────────────┘
```

## Components

### 🛠️ Tools

**Weather Tools (`weather_tools.py`):**
- `get_weather(city)` - Get current weather with temperature
- `get_forecast(city, days)` - Get multi-day forecast

**Greeter Tools (`greeter_tools.py`):**
- `create_greeting(name)` - Create personalized greeting
- `format_greeting_with_weather(name, weather_info)` - Combine greeting with weather

### 🤖 Agent

**Greeter Weather Agent (`greeter_weather_agent.py`):**
- Uses LangChain's ReAct (Reasoning + Acting) pattern
- Powered by OpenAI GPT-4o-mini
- Automatically selects and chains tools
- Transparent reasoning with Chain of Thought

### 🌐 API Server

**Flask API (`app.py`):**
- RESTful endpoints (`/health`, `/chat`)
- Streaming support (Server-Sent Events)
- Optional authentication
- Error handling and logging

### 🎨 Test Interface

**Streamlit App (`streamlit_test_app.py`):**
- Interactive chat interface
- Real-time streaming responses
- Chain of Thought visualization
- Connection testing
- Example prompts

## Files

```
langchain-agents/
├── greeter_weather_agent.py      # Main agent implementation
├── weather_tools.py               # Weather tools
├── greeter_tools.py               # Greeter tools
├── app.py                         # Flask API server
├── streamlit_test_app.py          # Streamlit test interface
├── requirements.txt               # Python dependencies
├── streamlit_requirements.txt     # Streamlit dependencies
├── Dockerfile                     # Container configuration
├── deploy_podman.sh              # Deployment automation
├── run_streamlit.sh              # Streamlit launcher
├── .env.example                  # Environment template
├── README.md                     # This file
├── QUICKSTART.md                 # Quick start guide
├── DEPLOYMENT.md                 # Deployment guide
└── TROUBLESHOOTING.md            # Troubleshooting guide
```

## Setup

### Prerequisites

- Docker, Podman, or Lima (with Docker)
- OpenAI API key
- Python 3.8+ (for local testing)

### Environment Configuration

Copy `.env.example` to `.env` in the project root and fill in your values:

```bash
cp .env.example .env
# Edit .env and add your API keys
```


### Deployment Options

#### Option 1: Lima (Docker in VM)

```bash
# Full deployment (recommended for macOS with Lima)
./deploy_lima.sh deploy

# Or step by step
./deploy_lima.sh build
./deploy_lima.sh start
```

#### Option 2: Podman

```bash
./deploy_podman.sh deploy
# Or step by step
./deploy_podman.sh build
./deploy_podman.sh start
```

#### Option 3: Docker

```bash
docker build -t langchain-greeter-agent .
docker run -d -p 5001:5000 --env-file .env langchain-greeter-agent
```

#### Option 4: Local (No Container)

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
python app.py
```

## Testing

### 1. Health Check

```bash
curl http://localhost:5001/health
```

### 2. Chat Endpoint

```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "My name is John and I am in New York"}
    ],
    "stream": false
  }'
```

### 3. Streamlit Interface

```bash
./run_streamlit.sh
```

Then open: http://localhost:8501

## Example Interactions

**Example 1:**
```
User: My name is John and I'm in New York
Agent: Hey hi John, welcome to the Agent System! The weather in New York is sunny with a temperature of 72°F
```

**Example 2:**
```
User: Hi, I'm Sarah from San Francisco
Agent: Hey hi Sarah, welcome to the Agent System! The weather in San Francisco is partly cloudy with a temperature of 68°F
```

**Example 3:**
```
User: I'm Mike in Chicago, what's the weather like?
Agent: Hey hi Mike, welcome to the Agent System! The weather in Chicago is cloudy with a temperature of 65°F
```

## Management Commands


### Lima/Podman/Docker

```bash
# View logs
./deploy_lima.sh logs   # or ./deploy_podman.sh logs

# Check status
./deploy_lima.sh status # or ./deploy_podman.sh status

# Restart
./deploy_lima.sh restart

# Stop
./deploy_lima.sh stop

# Remove everything
./deploy_lima.sh remove
```

### Streamlit

```bash
# Run Streamlit
./run_streamlit.sh

# Or manually
streamlit run streamlit_test_app.py --server.port 8501
```

## Key Features

✅ **Production Ready** - Containerized with Docker/Podman
✅ **OpenAI Powered** - Uses GPT-4o-mini for intelligence
✅ **Streaming Support** - Real-time responses via SSE
✅ **Chain of Thought** - Transparent reasoning process
✅ **Test Interface** - Beautiful Streamlit UI
✅ **Easy Deployment** - One-command deployment
✅ **No Auth Required** - Optional authentication
✅ **Error Handling** - Graceful error management
✅ **Comprehensive Docs** - Multiple guides included

## Customization

### Add New Tools

```python
from langchain.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """Tool description"""
    # Implementation
    return result

# Add to agent's tools list
tools = [get_weather, get_forecast, create_greeting, format_greeting_with_weather, my_custom_tool]
```

### Change LLM Model

Edit `greeter_weather_agent.py`:

```python
llm = ChatOpenAI(
    model="gpt-4",  # or "gpt-3.5-turbo"
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

### Adjust Agent Parameters

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,  # More iterations
    handle_parsing_errors=True
)
```

## Troubleshooting

### Common Issues

**Connection Refused:**
- Check if container is running: `./deploy_podman.sh status`
- View logs: `./deploy_podman.sh logs`

**500 Internal Server Error:**
- Verify OpenAI API key in `.env`
- Rebuild container: `./deploy_podman.sh remove && ./deploy_podman.sh deploy`

**Streamlit Can't Connect:**
- Verify agent is running: `curl http://localhost:5001/health`
- Check URL in Streamlit sidebar: `http://localhost:5001/chat`

**Import Errors:**
- Rebuild with fresh dependencies: `./deploy_podman.sh remove && ./deploy_podman.sh build`


## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## License
This project is provided as an example for learning purposes.

