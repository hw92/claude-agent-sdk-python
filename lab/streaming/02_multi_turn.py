#!/usr/bin/env python3
"""
Multi-Turn Conversation Example
Learn how to have a conversation with multiple back-and-forth turns
"""

import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)


async def multi_turn_chat():
    """Have a multi-turn conversation."""
    print("=== Multi-Turn Conversation ===\n")

    async with ClaudeSDKClient() as client:
        # First question
        print("User: What is the capital of Japan?")
        await client.query("What is the capital of Japan?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                break

        print()

        # Follow-up question (Claude remembers context)
        print("User: What is the population of that city?")
        await client.query("What is the population of that city?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                break

        print()

        # Third question
        print("User: What language do they speak there?")
        await client.query("What language do they speak there?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")


async def main():
    """Run the multi-turn example."""
    await multi_turn_chat()


if __name__ == "__main__":
    asyncio.run(main())
