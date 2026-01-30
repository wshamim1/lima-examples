# LangChain Greeter + Weather Agent (Lima Example)

A production-ready LangChain agent powered by OpenAI that combines greeting and weather functionality. Deployable with Lima, Docker, or Podman. Includes Streamlit test UI.

## 🚀 Quick Start

```bash
# 1. Copy environment template and edit
cp deploy-lanchain-agent/.env.example deploy-lanchain-agent/.env

# 2. Deploy with Lima (recommended for macOS)
cd deploy-lanchain-agent
./deploy_lima.sh deploy

# 3. Test with Streamlit
./run_streamlit.sh
```

**Access:** http://localhost:8501

## Features

- Greets users and fetches weather for their city
- Combines both into a personalized message
- Containerized API (Lima, Docker, Podman)
- Streamlit UI for testing
- Modular tools and agent logic

## Project Structure

```
build-deploy-flask-app/
  ...
deploy-lanchain-agent/
  app.py
  greeter_tools.py
  greeter_weather_agent.py
  weather_tools.py
  streamlit_app.py
  requirements.txt
  Dockerfile
  deploy_lima.sh
  deploy_podman.sh
  run_streamlit.sh
  .env.example
  README.md
```

## Environment Setup

- Copy `.env.example` to `.env` and fill in your API keys and config.
- Requires OpenAI API key and (optionally) a weather API key.

## Deployment Options

### 1. Lima (Docker in VM)

```bash
./deploy_lima.sh deploy
```

### 2. Podman

```bash
./deploy_podman.sh deploy
```

### 3. Docker

```bash
docker build -t langchain-greeter-agent .
docker run -d -p 5001:5000 --env-file .env langchain-greeter-agent
```

### 4. Local (No Container)

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
python app.py
```

## Management Commands (Lima/Podman)

```bash
./deploy_lima.sh logs    # Show logs
./deploy_lima.sh status  # Show status
./deploy_lima.sh stop    # Stop container
./deploy_lima.sh remove  # Remove container and image
```

## Testing

- Health: `curl http://localhost:5001/health`
- Chat: `curl -X POST http://localhost:5001/chat ...`
- Streamlit: `./run_streamlit.sh` and open http://localhost:8501

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

For detailed usage, see `deploy-lanchain-agent/README.md`.
