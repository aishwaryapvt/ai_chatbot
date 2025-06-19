from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
import streamlit as st

def initialize_agent():
    try:
        # Get config from Streamlit secrets
        model = ChatOpenAI(
            temperature=0,
            openai_api_key=st.secrets["OPENROUTER_API_KEY"],
            openai_api_base=st.secrets["OPENROUTER_API_BASE"],
            model=st.secrets.get("MODEL_NAME", "anthropic/claude-3-haiku"),
            streaming=True  # Ensure streaming is enabled
        )

        tools = [
            Tool.from_function(
                func=lambda x: str(eval(x)),
                name="Calculator",
                description="Useful for math calculations",
                args_schema=None
            )
        ]
        
        agent = create_react_agent(model, tools)
        
        # Verify the agent has streaming capability
        if not hasattr(agent, 'stream'):
            raise ValueError("Created agent doesn't support streaming")
            
        return agent
        
    except KeyError as e:
        raise ValueError(f"Missing configuration: {str(e)}")
    except Exception as e:
        raise ValueError(f"Agent creation failed: {str(e)}")