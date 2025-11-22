#!/usr/bin/env python3
"""
Simple Calculator Tool Example
Learn how to create basic MCP tools using the @tool decorator
"""

import asyncio
from typing import Any

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)


# Define a simple calculator tool
@tool("add", "Add two numbers together", {"a": float, "b": float})
async def add_tool(args: dict[str, Any]) -> dict[str, Any]:
    """Simple addition tool."""
    result = args["a"] + args["b"]
    return {
        "content": [{"type": "text", "text": f"Result: {args['a']} + {args['b']} = {result}"}]
    }


@tool("multiply", "Multiply two numbers", {"a": float, "b": float})
async def multiply_tool(args: dict[str, Any]) -> dict[str, Any]:
    """Simple multiplication tool."""
    result = args["a"] * args["b"]
    return {
        "content": [{"type": "text", "text": f"Result: {args['a']} × {args['b']} = {result}"}]
    }


async def main():
    """Run the simple calculator example."""

    # Step 1: Create the MCP server with our tools
    calculator = create_sdk_mcp_server(
        name="simple_calc",
        version="1.0.0",
        tools=[add_tool, multiply_tool],
    )

    # Step 2: Configure options to use our calculator
    options = ClaudeAgentOptions(
        mcp_servers={"calc": calculator},
        allowed_tools=[
            "mcp__calc__add",
            "mcp__calc__multiply",
        ],
    )

    # Step 3: Use the calculator
    prompts = [
        "Add 5 and 7",
        "Multiply 6 by 8",
    ]

    for prompt in prompts:
        print(f"\n{'='*40}")
        print(f"Prompt: {prompt}")
        print('='*40)

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Claude: {block.text}")
                        elif isinstance(block, ToolUseBlock):
                            print(f"[Using tool: {block.name}]")


if __name__ == "__main__":
    asyncio.run(main())
