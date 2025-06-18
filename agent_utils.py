import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

def initialize_agent():
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
            description="Useful for math calculations"
        )
    ]
    
    return create_react_agent(model, tools)
