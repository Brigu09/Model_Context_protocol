import streamlit as st
import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import nest_asyncio

# Apply asyncio fix for nested event loops
nest_asyncio.apply()

# Fix for Windows event loop compatibility with subprocesses
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize MCPClient and agent only once
if "agent" not in st.session_state:
    config = "mcp_server_config.json"
    client = MCPClient.from_dict(config)
    llm = ChatGroq(model="qwen-qwq-32b")
    st.session_state.agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=30,
        memory_enabled=True
    )

# Streamlit UI
st.title("🤖 Agentic AI System with MCP Server")
st.write("Ask anything, and your AI agent will handle it with memory!")

user_input = st.text_input("Your query", placeholder="e.g., Find the best restaurant in San Francisco")

if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Thinking..."):
            async def get_response():
                return await st.session_state.agent.run(user_input)

            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(get_response())

        st.success("Response:")
        st.write(response)
