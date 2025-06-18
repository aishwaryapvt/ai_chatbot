import streamlit as st
from agent_utils import initialize_agent
from langchain_core.messages import HumanMessage

# PAGE CONFIG MUST COME FIRST
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agent (after page config)
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()
    if st.session_state.agent is None:
        st.error("Failed to initialize AI agent. Please check your configuration.")
        st.stop()

# Sidebar - must come after page config
with st.sidebar:
    st.header("Settings")
    st.markdown("Using OpenRouter API")
    st.divider()
    st.markdown("**Note:** Calculator supports basic math expressions")

# Main chat interface
st.title("🤖 AI Assistant")
st.caption("Ask me anything or use the calculator")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        for chunk in st.session_state.agent.stream(
            {"messages": [HumanMessage(content=prompt)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    full_response += message.content
                    response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
