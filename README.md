# LangChain Greeter + Weather Agent & Build/Deploy Flask App (Lima Example)

A production-ready LangChain agent powered by OpenAI that combines greeting and weather functionality. Deployable with Lima, Docker, or Podman. Includes Streamlit test UI.

## 🚀 Quick Start Guide

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
  flask_app/
    app.py
    requirements.txt
    Dockerfile
    templates/
      form.html
  docker-compose.yml
  README.md
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

---

# About `build-deploy-flask-app`

This directory contains a simple Flask web application with a MySQL backend, orchestrated using Docker Compose.

**Features:**
- Submit user data (name, email) via a web form
- Store submissions in a MySQL database
- Fetch and display all users in a table

**How to Run:**
1. Navigate to the directory:
   ```sh
   cd build-deploy-flask-app
   ```
2. Build and start the services:
   ```sh
   docker-compose up --build
   ```
3. Visit [http://localhost:5000](http://localhost:5000) in your browser.

See `build-deploy-flask-app/README.md` for more details and environment variable configuration.

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
