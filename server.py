#!/usr/bin/env python3
"""
Simple MCP Echo Server
A basic MCP server that echoes back any input it receives.

This server communicates using the Model Context Protocol (MCP) over stdio.
It expects JSON-RPC formatted messages, not plain text input.

To test this server, use a proper MCP client or the test_client.py script.
"""

import asyncio
import json
import sys
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)


# Create server instance
app = Server("echo-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echoes back the input text you provide",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                },
                "required": ["message"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "echo":
        message = arguments.get("message", "")
        return [
            TextContent(
                type="text",
                text=f"Echo: {message}"
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the server."""
    logger = logging.getLogger(__name__)

    # Warn if running in interactive terminal
    if sys.stdin.isatty():
        logger.warning("=" * 70)
        logger.warning("WARNING: This MCP server expects JSON-RPC messages over stdin.")
        logger.warning("Typing plain text will cause validation errors.")
        logger.warning("Please use a proper MCP client or run: python test_client.py")
        logger.warning("=" * 70)

    logger.info("MCP Echo Server starting...")

    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
