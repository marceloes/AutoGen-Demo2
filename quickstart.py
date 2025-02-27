#pip install autogen-agentchat
#pip install autogen-ext[azure]
#pip install autogen?

import os
import autogen
from autogen import AssistantAgent, UserProxyAgent

print (os.getenv("OPENAI_API_KEY"))
print (os.getenv("AZURE_OPENAI_ENDPOINT"))

llm_config = {
    "model": "gpt-4o-mini", 
    "api_key": os.getenv("OPENAI_API_KEY"), 
    "api_type": "azure", 
    "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "api_version": "2025-01-01-preview"
    }
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config)

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding_workdir")}
)

# Start the chat
user_proxy.initiate_chat(
    assistant, 
    message="Plot a chart of NVDA and TESLA stock price changes YTD using Yahoo Finance. Add the EST timezone when calling the API."
)
