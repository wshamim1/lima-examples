"""
LangChain Greeter + Weather Agent with OpenAI
Combines greeting and weather functionality using LangChain agents
"""
import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from weather_tools import get_weather, get_forecast
from greeter_tools import create_greeting, format_greeting_with_weather

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
def get_openai_llm():
    """Initialize and return OpenAI LLM"""
    return ChatOpenAI(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo" for faster/cheaper
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# Define the agent prompt
AGENT_PROMPT = """You are a friendly greeter agent that welcomes users and provides weather information.

You have access to the following tools:

{tools}

Tool Names: {tool_names}

Your workflow:
1. When a user provides their name and city, greet them warmly
2. Get the current weather for their city
3. Combine the greeting with weather information

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

def create_greeter_agent():
    """Create and return the greeter + weather agent"""
    
    # Get LLM
    llm = get_openai_llm()
    
    # Combine all tools
    tools = [
        get_weather,
        get_forecast,
        create_greeting,
        format_greeting_with_weather
    ]
    
    # Create prompt template
    prompt = PromptTemplate.from_template(AGENT_PROMPT)
    
    # Create agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    return agent_executor

def run_agent(user_input: str):
    """Run the agent with user input"""
    agent_executor = create_greeter_agent()
    
    try:
        result = agent_executor.invoke({"input": user_input})
        return result.get("output", result.get("result", ""))
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("LangChain Greeter + Weather Agent (OpenAI)")
    print("=" * 60)
    print()
    
    # Test cases
    test_inputs = [
        "My name is John and I'm in New York",
        "Hi, I'm Sarah from San Francisco",
        "I'm Mike in Chicago, what's the weather like?"
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        print("-" * 60)
        response = run_agent(user_input)
        print(f"Agent: {response}")
        print("=" * 60)

