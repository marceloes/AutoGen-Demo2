import asyncio
#from autogen_ext.models.openai import OpenAIChatCompletionClient
#from autogen_ext.models.azure import AzureAIChatCompletionClient
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.models import UserMessage

from azure.core.credentials import AzureKeyCredential
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

import os
from dotenv import load_dotenv
load_dotenv()

async def main() -> None:
    # model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    model_client = AzureOpenAIChatCompletionClient(
        azure_deployment="gpt-4o-mini",
        model="gpt-4o-mini",
        api_version="2025-01-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    async def get_weather(location: str) -> str:
        return f"The weather in {location} is sunny."

    assistant = AssistantAgent(
        "Assistant",
        model_client=model_client,
        tools=[get_weather],
    )

    #result = await model_client.create([UserMessage(content="What's the weather in New York?", source="user")])
    termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat([assistant], termination_condition=termination)
    await Console(team.run_stream(task="What's the weather in New York?"))


asyncio.run(main())