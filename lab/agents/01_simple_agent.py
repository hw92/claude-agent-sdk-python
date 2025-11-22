#!/usr/bin/env python3
"""
Simple Agent Example
Learn how to define and use custom agents with specific roles
"""

import anyio

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)


async def summarizer_agent():
    """Create a simple summarizer agent."""
    print("=== Summarizer Agent ===\n")

    # Define a custom agent with specific role
    options = ClaudeAgentOptions(
        agents={
            "summarizer": AgentDefinition(
                description="Summarizes text in bullet points",
                prompt="You are a summarizer. Given any text, provide a concise "
                       "summary in 3-5 bullet points. Be brief and clear.",
                tools=["Read"],  # Can read files if needed
                model="haiku",   # Use faster/cheaper model for simple tasks
            ),
        },
    )

    async for message in query(
        prompt="Use the summarizer agent to explain what Python is",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage) and message.total_cost_usd:
            print(f"\nCost: ${message.total_cost_usd:.4f}")
    print()


async def helper_agent():
    """Create a simple helper agent."""
    print("=== Helper Agent ===\n")

    options = ClaudeAgentOptions(
        agents={
            "helper": AgentDefinition(
                description="A friendly assistant that answers questions",
                prompt="You are a friendly helper. Answer questions in a simple, "
                       "conversational way. Keep responses short and helpful.",
                tools=[],  # No special tools needed
            ),
        },
    )

    async for message in query(
        prompt="Use the helper agent to explain what async/await means in Python",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def main():
    """Run agent examples."""
    await summarizer_agent()
    await helper_agent()


if __name__ == "__main__":
    anyio.run(main)
