# Claude Agent SDK - Learning Summary

**Date:** 2026-01-03  
**Author:** Hai  
**Purpose:** Understanding Claude Agent SDK for AI Investment Application

---

## Table of Contents

1. [What is Claude Agent SDK?](#what-is-claude-agent-sdk)
2. [Core Concepts](#core-concepts)
3. [Architecture Overview](#architecture-overview)
4. [Custom Tools (MCP Servers)](#custom-tools-mcp-servers)
5. [Session Management](#session-management)
6. [Cost Analysis](#cost-analysis)
7. [Investment App Use Cases](#investment-app-use-cases)
8. [Best Practices](#best-practices)

---

## What is Claude Agent SDK?

The Claude Agent SDK is a Python library that enables **agentic AI behavior** with Claude. It wraps the Claude Code CLI and provides:

- ✅ **Tool execution** - File I/O, bash commands, custom functions
- ✅ **Multi-step reasoning** - Claude can plan and execute complex workflows
- ✅ **MCP integration** - Create custom tools as in-process servers
- ✅ **Hooks** - Add custom logic at specific points in the agent loop
- ✅ **Session management** - Maintain conversation context

### Installation

```bash
pip install claude-agent-sdk
```

The Claude Code CLI is **automatically bundled** - no separate installation needed!

---

## Core Concepts

### 1. Query Function (Simple Usage)

For one-off queries without custom tools:

```python
import anyio
from claude_agent_sdk import query, AssistantMessage, TextBlock

async def main():
    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

anyio.run(main())
```

### 2. ClaudeSDKClient (Advanced Usage)

For interactive conversations with custom tools and hooks:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write"],
    max_turns=5
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Create a hello.py file")
    async for message in client.receive_response():
        print(message)
```

### 3. Custom Agents

Define specialized agents for specific tasks:

```python
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions

options = ClaudeAgentOptions(
    agents={
        "market-analyst": AgentDefinition(
            description="Analyzes market trends and stocks",
            prompt="You are a market analyst expert. Analyze financial data...",
            tools=["Read", "Bash"],
            model="sonnet",
        ),
    },
)
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Your Python Application                     │
├─────────────────────────────────────────────────────────────────┤
│  ClaudeSDKClient                                                │
│  ├── Custom Agents (specialized behaviors)                      │
│  ├── Built-in Tools (Read, Write, Bash, Grep, Glob)             │
│  └── MCP Servers (Custom Tools - in-process!)                   │
│      ├── get_stock_price() → Your data API                      │
│      ├── get_portfolio() → Your database                        │
│      └── calculate_risk() → Your risk engine                    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code CLI (Bundled)                    │
│  • Manages conversation state                                   │
│  • Routes tool calls                                            │
│  • Handles permissions                                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Anthropic API                              │
│  • Claude Sonnet 4 model                                        │
│  • Prompt caching enabled                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Custom Tools (MCP Servers)

### What are MCP Servers?

**MCP (Model Context Protocol)** servers provide tools that Claude can invoke. The SDK allows you to create **in-process** MCP servers (no separate processes needed!).

### Creating Custom Tools

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

# Step 1: Define tools with @tool decorator
@tool("get_stock_price", "Get current stock price", {"symbol": str})
async def get_stock_price(args):
    symbol = args['symbol']
    # Your logic to fetch stock prices
    price = await fetch_from_api(symbol)
    return {
        "content": [
            {"type": "text", "text": f"Current price of {symbol}: ${price}"}
        ]
    }

@tool("get_portfolio", "Get user's portfolio", {"user_id": str})
async def get_portfolio(args):
    holdings = await fetch_user_holdings(args['user_id'])
    return {"content": [{"type": "text", "text": str(holdings)}]}

# Step 2: Create SDK MCP server
investment_server = create_sdk_mcp_server(
    name="investment-tools",
    version="1.0.0",
    tools=[get_stock_price, get_portfolio]
)

# Step 3: Configure options
options = ClaudeAgentOptions(
    mcp_servers={"inv": investment_server},
    allowed_tools=[
        "mcp__inv__get_stock_price",
        "mcp__inv__get_portfolio"
    ]
)

# Step 4: Use with client
async with ClaudeSDKClient(options=options) as client:
    await client.query("What's AAPL's price and show my portfolio?")
    async for msg in client.receive_response():
        print(msg)
```

### Tool Naming Convention

Format: `mcp__<server_alias>__<tool_name>`

Example: `mcp__inv__get_stock_price`
- `mcp__` - Prefix for MCP tools
- `inv` - Server alias (from `mcp_servers={"inv": ...}`)
- `get_stock_price` - Tool name

### Benefits Over External MCP Servers

| In-Process SDK Server | External MCP Server |
|----------------------|---------------------|
| ✅ Same Python process | ❌ Separate process |
| ✅ No IPC overhead | ❌ IPC communication |
| ✅ Easier debugging | ❌ Complex debugging |
| ✅ Simple deployment | ❌ Multiple processes |
| ✅ Direct function calls | ❌ JSON-RPC protocol |

---

## Session Management

### Key Insight: ClaudeSDKClient = CLI Session

```python
# Each ClaudeSDKClient instance = One conversation session
async with ClaudeSDKClient(options=options) as client:
    # Session starts (CLI process spawned)
    
    await client.query("What's AAPL?")
    # Claude responds
    
    await client.query("What's MSFT?")
    # Claude remembers previous query!
    
    await client.query("Compare them")
    # Claude has full conversation context
    
# Session ends (CLI process terminated)
```

### Context Sharing

```python
# ❌ NO CONTEXT SHARING (new client each time)
for prompt in prompts:
    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        # Each iteration = fresh conversation

# ✅ CONTEXT SHARING (single client)
async with ClaudeSDKClient(options=options) as client:
    for prompt in prompts:
        await client.query(prompt)
        # All queries share context!
```

### Execution Flow

```
User: "Calculate 15 + 27"
    ↓
ClaudeSDKClient → Sends to Claude Code CLI
    ↓
Claude Agent → Understands it needs calculator tool
    ↓
MCP Server → Executes add_numbers(15, 27)
    ↓
Returns: "15 + 27 = 42"
    ↓
Claude Agent → Formulates response
    ↓
ClaudeSDKClient → Streams back to user
    ↓
Output: "Claude: 15 + 27 = 42"
```

---

## Cost Analysis

### Pricing (Claude Sonnet 4)

| Token Type | Regular | Cache Write | Cache Read |
|------------|---------|-------------|------------|
| Input | $3.00/MTok | $3.75/MTok | $0.30/MTok (90% off!) |
| Output | $15.00/MTok | N/A | N/A |

### Agent SDK Overhead

**Per Request Overhead: ~2500-3000 tokens**

Components:
- System prompt: ~1000 tokens
- Tool definitions: ~500-1000 tokens (built-in)
- MCP schemas: ~300-900 tokens (custom tools)
- Guidelines: ~200-400 tokens

### Cost Comparison

#### Single Query

```
Direct API:
- Input: 100 tokens × $3/MTok = $0.0003

Agent SDK (first turn):
- Input: 2750 tokens × $3.75/MTok = $0.0103
- Overhead: 34x more expensive!

Agent SDK (cached turn):
- Input: 2750 tokens (2650 cached @ $0.30, 100 @ $3) = $0.0011
- Overhead: 3.7x more expensive
```

#### 10-Turn Session

```
Direct API:
- Total: ~$0.025

Agent SDK (with caching):
- Total: ~$0.045
- 1.8x more expensive, but fully automated!
```

### Prompt Caching Magic

```
Turn 1: Write cache
├─ System prompt: 1000 tokens @ $3.75/MTok = $0.00375
├─ Tools: 2000 tokens @ $3.75/MTok = $0.0075
└─ Prompt: 100 tokens @ $3/MTok = $0.0003
Total: $0.01155

Turn 2: Read cache (90% discount!)
├─ System prompt: 1000 tokens @ $0.30/MTok = $0.0003
├─ Tools: 2000 tokens @ $0.30/MTok = $0.0006
├─ History: 500 tokens @ $3/MTok = $0.0015
└─ Prompt: 100 tokens @ $3/MTok = $0.0003
Total: $0.0027

Savings: 77% cheaper on turn 2!
```

**Cache Duration:** 5 minutes (refreshed on each use)

### When Agent SDK is Worth It

✅ **Use Agent SDK when:**
- Multi-turn conversations
- Need tool execution (file I/O, bash, custom tools)
- Complex workflows with multiple steps
- Automated data fetching
- Long sessions (caching benefits)

❌ **Use Direct API when:**
- Simple Q&A (no tools)
- Single query
- Static data already available
- Cost is critical
- No need for automation

---

## Investment App Use Cases

### 1. Stock Analysis Agent

```python
@tool("get_stock_price", "Get current stock price", {"symbol": str})
async def get_stock_price(args):
    # Fetch from Yahoo Finance, Alpha Vantage, etc.
    pass

@tool("get_fundamentals", "Get company fundamentals", {"symbol": str})
async def get_fundamentals(args):
    # Fetch P/E, EPS, revenue, etc.
    pass

@tool("get_news", "Get recent news", {"symbol": str})
async def get_news(args):
    # Fetch news articles
    pass

investment_server = create_sdk_mcp_server(
    name="stock-analysis",
    tools=[get_stock_price, get_fundamentals, get_news]
)
```

### 2. Portfolio Management Agent

```python
@tool("get_portfolio", "Get user portfolio", {"user_id": str})
async def get_portfolio(args):
    # Fetch from database
    pass

@tool("calculate_risk", "Calculate portfolio risk", {"portfolio": dict})
async def calculate_risk(args):
    # Your risk calculation engine
    pass

@tool("suggest_rebalance", "Suggest rebalancing", {"portfolio": dict})
async def suggest_rebalance(args):
    # Your optimization algorithm
    pass
```

### 3. Multi-Agent Investment System

```python
options = ClaudeAgentOptions(
    agents={
        "market-analyst": AgentDefinition(
            description="Analyzes market trends",
            prompt="You are a market analyst. Analyze trends and patterns.",
            tools=["mcp__stock__get_price", "mcp__stock__get_news"],
            model="sonnet",
        ),
        "portfolio-advisor": AgentDefinition(
            description="Provides portfolio recommendations",
            prompt="You are a portfolio advisor. Evaluate risk and diversification.",
            tools=["mcp__portfolio__get_portfolio", "mcp__portfolio__calculate_risk"],
            model="sonnet",
        ),
        "risk-manager": AgentDefinition(
            description="Assesses investment risks",
            prompt="You are a risk manager. Identify and quantify risks.",
            tools=["mcp__portfolio__calculate_risk"],
            model="sonnet",
        ),
    },
)
```

### 4. Compliance Hooks

```python
async def compliance_check(input_data, tool_use_id, context):
    """Block trading actions without confirmation."""
    tool_name = input_data["tool_name"]
    if tool_name in ["execute_trade", "place_order"]:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Trading requires explicit confirmation",
            }
        }
    return {}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[compliance_check]),
        ],
    }
)
```

---

## Best Practices

### 1. Session Management

```python
# ✅ Keep sessions alive for related queries
async with ClaudeSDKClient(options=options) as client:
    # User's investment analysis session
    await client.query("What's AAPL's price?")
    await client.query("What's the P/E ratio?")
    await client.query("Should I buy?")
    # All queries share context and benefit from caching

# ❌ Don't create new sessions unnecessarily
for query in queries:
    async with ClaudeSDKClient(options=options) as client:
        await client.query(query)
        # Cache expires, no context sharing
```

### 2. Minimize Tool Overhead

```python
# ✅ Only include necessary tools
options = ClaudeAgentOptions(
    allowed_tools=[
        "mcp__inv__get_stock_price",
        "mcp__inv__get_portfolio"
    ]
)

# ❌ Don't include all tools if not needed
options = ClaudeAgentOptions(
    allowed_tools=["*"]  # Adds ~2000 tokens overhead!
)
```

### 3. Error Handling in Tools

```python
@tool("divide", "Divide numbers", {"a": float, "b": float})
async def divide_numbers(args):
    if args["b"] == 0:
        return {
            "content": [{"type": "text", "text": "Error: Division by zero"}],
            "is_error": True  # Mark as error
        }
    result = args["a"] / args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}
```

### 4. Cost Optimization

```python
# Use max_turns to limit iterations
options = ClaudeAgentOptions(
    max_turns=5,  # Prevent runaway costs
    allowed_tools=["mcp__inv__get_stock_price"]
)

# Use max_budget_usd for hard limits
options = ClaudeAgentOptions(
    max_budget_usd=0.50  # Stop at $0.50
)
```

### 5. Virtual Environment

Always use a virtual environment to avoid dependency conflicts:

```bash
python -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk
```

---

## Key Takeaways

1. **ClaudeSDKClient = CLI Session** - Each instance is a conversation with context
2. **MCP Tools = In-Process Functions** - No separate processes, just async Python functions
3. **Prompt Caching Saves 90%** - System prompts and tools are cached after first turn
4. **Overhead is ~2500 tokens** - But worth it for multi-turn tool-based workflows
5. **Tool Naming: `mcp__<alias>__<name>`** - Follow this convention for custom tools
6. **Context Sharing Requires Same Client** - Don't create new clients for each query
7. **Cache Lasts 5 Minutes** - Keep sessions alive to benefit from caching

---

## Next Steps

1. ✅ Explore examples in `/examples` directory
2. ✅ Build custom MCP tools for your investment data sources
3. ✅ Design specialized agents for different investment tasks
4. ✅ Add compliance hooks for safety
5. ✅ Test cost optimization strategies
6. ✅ Integrate into your investment application

---

## Resources

- [Official Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)
- [GitHub Repository](https://github.com/anthropics/claude-agent-sdk)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Examples Directory](/examples)

---

**Happy Building! 🚀**
