import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

load_dotenv()

async def main():
    config = "mcp_server_config.json"
    client = MCPClient.from_dict(config)
    llm = ChatGroq(model="qwen-qwq-32b")
    agent = MCPAgent(llm=llm, client=client, max_steps=30, memory_enabled=True)

    response = await agent.run("Tell me a joke about AI.")
    print(response)



asyncio.run(main())
