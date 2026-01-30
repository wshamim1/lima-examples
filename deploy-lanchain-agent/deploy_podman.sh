#!/bin/bash

# Podman Deployment Script for LangChain Greeter + Weather Agent
# This script builds and runs the agent as a container using Podman

set -e

# Configuration
IMAGE_NAME="langchain-greeter-agent"
CONTAINER_NAME="langchain-greeter-agent"
PORT=5001
HOST_PORT=5001

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== LangChain Agent Podman Deployment ===${NC}"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found in project root${NC}"
   
    exit 1
fi

# Function to build image
build_image() {
    echo -e "${BLUE}Building Podman image...${NC}"
    podman build -t ${IMAGE_NAME}:latest .
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Image built successfully${NC}"
    else
        echo -e "${RED}✗ Failed to build image${NC}"
        exit 1
    fi
}

# Function to stop and remove existing container
stop_container() {
    echo -e "${BLUE}Checking for existing container...${NC}"
    if podman ps -a | grep -q ${CONTAINER_NAME}; then
        echo -e "${YELLOW}Stopping and removing existing container...${NC}"
        podman stop ${CONTAINER_NAME} 2>/dev/null || true
        podman rm ${CONTAINER_NAME} 2>/dev/null || true
        echo -e "${GREEN}✓ Existing container removed${NC}"
    fi
}

# Function to run container
run_container() {
    echo -e "${BLUE}Starting container...${NC}"
    podman run -d \
        --name ${CONTAINER_NAME} \
        -p ${HOST_PORT}:${PORT} \
        --env-file .env \
        ${IMAGE_NAME}:latest
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Container started successfully${NC}"
        echo ""
        echo -e "${GREEN}Container Details:${NC}"
        echo "  Name: ${CONTAINER_NAME}"
        echo "  Port: ${HOST_PORT}"
        echo "  URL: http://localhost:${HOST_PORT}"
        echo ""
        echo -e "${YELLOW}Test the API:${NC}"
        echo "  curl http://localhost:${HOST_PORT}/health"
    else
        echo -e "${RED}✗ Failed to start container${NC}"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}Container logs:${NC}"
    podman logs -f ${CONTAINER_NAME}
}

# Function to show status
show_status() {
    echo -e "${BLUE}Container status:${NC}"
    podman ps -a | grep ${CONTAINER_NAME} || echo "Container not found"
}

# Main menu
case "$1" in
    build)
        build_image
        ;;
    start)
        stop_container
        run_container
        ;;
    stop)
        echo -e "${BLUE}Stopping container...${NC}"
        podman stop ${CONTAINER_NAME}
        echo -e "${GREEN}✓ Container stopped${NC}"
        ;;
    restart)
        stop_container
        run_container
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    remove)
        echo -e "${BLUE}Removing container and image...${NC}"
        podman stop ${CONTAINER_NAME} 2>/dev/null || true
        podman rm ${CONTAINER_NAME} 2>/dev/null || true
        podman rmi ${IMAGE_NAME}:latest 2>/dev/null || true
        echo -e "${GREEN}✓ Cleanup complete${NC}"
        ;;
    deploy)
        build_image
        echo ""
        stop_container
        echo ""
        run_container
        ;;
    *)
        echo "Usage: $0 {build|start|stop|restart|logs|status|remove|deploy}"
        echo ""
        echo "Commands:"
        echo "  build    - Build the Podman image"
        echo "  start    - Start the container"
        echo "  stop     - Stop the container"
        echo "  restart  - Restart the container"
        echo "  logs     - Show container logs"
        echo "  status   - Show container status"
        echo "  remove   - Remove container and image"
        echo "  deploy   - Build and start (full deployment)"
        exit 1
        ;;
esac

