import streamlit as st
from agent_utils import initialize_agent
from langchain_core.messages import HumanMessage

# 1. Page config must be first
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# 2. Initialize session state
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

# 3. Show error if agent failed
if st.session_state.agent is None:
    st.error("AI service unavailable. Check your configuration.")
    st.stop()

# 4. UI Elements (static parts)
with st.sidebar:
    st.header("Settings")
    st.markdown("Using OpenRouter API")
    st.divider()
    st.markdown("**Note:** Calculator supports basic math expressions")

st.title("🤖 AI Assistant")
st.caption("Ask me anything or use the calculator")

# 5. Display existing messages FIRST
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle new input LAST
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            response_placeholder = st.empty()
            full_response = ""
            
            for chunk in st.session_state.agent.stream(
                {"messages": [HumanMessage(content=prompt)]}
            ):
                if isinstance(chunk, dict) and "agent" in chunk:
                    for message in chunk["agent"]["messages"]:
                        full_response += message.content
                        response_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"AI response error: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error"})
