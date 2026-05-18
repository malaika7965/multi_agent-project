import streamlit as st
import os
from dotenv import load_dotenv
from graph import compiled_graph

# .env file se variables load karne ke liye
load_dotenv()

# Check karein ke API key mojood hai ya nahi
api_key = os.getenv("GROQ_API_KEY")

# Streamlit App Custom Style & Configuration
st.set_page_config(page_title="UOS AI Helpdesk", page_icon="🎓", layout="wide")

# Sidebar Structure
st.sidebar.markdown("<h1 style='text-align: center; font-size: 70px; margin-top: -30px;'>🎓</h1>", unsafe_allow_html=True)
st.sidebar.title("System Dashboard")

# Status UI Indicators (Bina hardcoded key ke)
if api_key:
    st.sidebar.success("Groq API: Connected ✅")
else:
    st.sidebar.error("Groq API: Missing ❌ Check .env")

st.sidebar.info("Scraper Mode: Live Web Target")

# Main Interface
st.title("🏛️ University of Sahiwal AI Helpdesk")
st.write("Welcome to the official multi-agent helpdesk. Ask anything about courses, admissions, or faculty.")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input Panel
if user_query := st.chat_input("Ask about admissions, fee structure, programs..."):
    # Display user query
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Process through LangGraph Multi-Agent Workflow
    with st.chat_message("assistant"):
        with st.spinner("Agents are analyzing & searching web..."):
            try:
                # Graph state input
                initial_state = {
                    "user_query": user_query,
                    "query_type": "",
                    "retrieved_context": "",
                    "agent_response": "",
                    "evaluation_result": ""
                }
                
                # Execution
                final_output = compiled_graph.invoke(initial_state)
                response_text = final_output["agent_response"]
                
                st.write(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                error_msg = f"System Error: Connection or execution failed. Details: {str(e)}"
                st.error(error_msg)