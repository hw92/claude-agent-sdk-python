#!/usr/bin/env python3
"""
Basic Streaming Example
Learn how to use ClaudeSDKClient for streaming responses
"""

import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)


async def simple_streaming():
    """Basic streaming with context manager."""
    print("=== Simple Streaming ===\n")

    # Using async context manager ensures proper cleanup
    async with ClaudeSDKClient() as client:
        # Send a query
        await client.query("What is 2 + 2?")

        # Stream the response
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                print("[Response complete]")

    print()


async def streaming_with_cost():
    """Streaming that shows the cost."""
    print("=== Streaming with Cost ===\n")

    async with ClaudeSDKClient() as client:
        await client.query("Tell me a one-liner joke")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd:
                    print(f"\nCost: ${message.total_cost_usd:.6f}")

    print()


async def main():
    """Run streaming examples."""
    await simple_streaming()
    await streaming_with_cost()


if __name__ == "__main__":
    asyncio.run(main())
