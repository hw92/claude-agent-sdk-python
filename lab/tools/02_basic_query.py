#!/usr/bin/env python3
"""
Basic Query Example
Learn the simplest way to interact with Claude Agent SDK
"""

import anyio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    query,
)


async def simple_question():
    """Ask a simple question using the query function."""
    print("=== Simple Question ===\n")

    # The simplest way to use Claude
    async for message in query(prompt="What is the capital of France?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def question_with_options():
    """Ask a question with custom options."""
    print("=== Question with Options ===\n")

    # Configure custom behavior
    options = ClaudeAgentOptions(
        system_prompt="You are a friendly tutor. Explain things simply.",
        max_turns=1,  # Limit to one response
    )

    async for message in query(
        prompt="Explain what an API is in one sentence.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def main():
    """Run all basic query examples."""
    await simple_question()
    await question_with_options()


if __name__ == "__main__":
    anyio.run(main)
