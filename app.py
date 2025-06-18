import streamlit as st
from agent_utils import initialize_agent
from langchain_core.messages import HumanMessage

# Must be the first Streamlit command
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize with proper error handling
if "agent" not in st.session_state:
    try:
        st.session_state.agent = initialize_agent()
        if not hasattr(st.session_state.agent, 'stream'):
            raise AttributeError("Agent doesn't support streaming")
    except Exception as e:
        st.error(f"Agent initialization failed: {str(e)}")
        st.session_state.agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show error if agent failed to initialize
if st.session_state.agent is None:
    st.error("""
    AI service unavailable. Please check:
    1. Your API key in Streamlit Secrets
    2. Your internet connection
    3. The model availability
    """)
    st.stop()

# Rest of your UI code...

# Updated chat input section with better error handling
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response_placeholder = st.empty()
            full_response = ""
            
            for chunk in st.session_state.agent.stream(
                {"messages": [HumanMessage(content=prompt)]}
            ):
                # Handle different response formats
                if hasattr(chunk, "messages"):  # For newer agent versions
                    for message in chunk.messages:
                        full_response += message.content
                elif isinstance(chunk, dict):  # For older versions
                    if "agent" in chunk and "messages" in chunk["agent"]:
                        for message in chunk["agent"]["messages"]:
                            full_response += message.content
                
                response_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"AI response error: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error"})

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

