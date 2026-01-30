#!/bin/bash

# Run Streamlit Test App for LangChain Agent
# This script sets up and runs the Streamlit testing interface

set -e

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== LangChain Agent Streamlit Tester ===${NC}"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}Streamlit not found. Installing dependencies...${NC}"
    pip install -r streamlit_requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
fi

# Check if agent is running
echo -e "${BLUE}Checking if agent is running...${NC}"
if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Agent is running at http://localhost:5001${NC}"
else
    echo -e "${YELLOW}⚠ Agent is not running at http://localhost:5001${NC}"
    echo -e "${YELLOW}Start the agent with: ./deploy_podman.sh deploy${NC}"
fi

echo ""
echo -e "${BLUE}Starting Streamlit app...${NC}"
echo -e "${GREEN}Access the app at: http://localhost:8501${NC}"
echo ""

# Run streamlit
streamlit run streamlit_app.py --server.port 8501 --server.address localhost

