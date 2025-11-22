#!/usr/bin/env python3
"""
Multi-Agent Example
Learn how to define multiple agents that can work together
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


async def multi_agent_team():
    """Create a team of agents with different specialties."""
    print("=== Multi-Agent Team ===\n")

    # Define multiple agents with different roles
    options = ClaudeAgentOptions(
        agents={
            # Researcher agent - finds and reads information
            "researcher": AgentDefinition(
                description="Researches and gathers information from files",
                prompt="You are a researcher. Find and analyze information. "
                       "Report your findings in a structured way.",
                tools=["Read", "Grep", "Glob"],
                model="haiku",
            ),
            # Explainer agent - explains concepts simply
            "explainer": AgentDefinition(
                description="Explains technical concepts in simple terms",
                prompt="You are a teacher. Explain technical concepts in simple, "
                       "easy-to-understand language. Use analogies when helpful.",
                tools=["Read"],
                model="haiku",
            ),
        },
    )

    # Use the researcher agent
    print("--- Using Researcher Agent ---")
    async for message in query(
        prompt="Use the researcher agent to find Python files in the examples directory",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage) and message.total_cost_usd:
            print(f"\nCost: ${message.total_cost_usd:.4f}")

    print()


async def main():
    """Run multi-agent examples."""
    await multi_agent_team()


if __name__ == "__main__":
    anyio.run(main)
