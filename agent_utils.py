import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
import streamlit as st

def initialize_agent():
    try:
        load_dotenv()
        
        # Validate environment variables
        required_vars = ["OPENROUTER_API_KEY", "OPENROUTER_API_BASE", "MODEL_NAME"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

        model = ChatOpenAI(
            temperature=0,
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base=os.getenv("OPENROUTER_API_BASE"),
            model=os.getenv("MODEL_NAME")
        )

        tools = [
            Tool.from_function(
                func=lambda x: str(eval(x)),
                name="Calculator",
                description="Useful for math calculations",
                args_schema=None
            )
        ]
        
        return create_react_agent(model, tools)
        
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return None
