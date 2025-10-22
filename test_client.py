#!/usr/bin/env python3
"""
Test client for the MCP Echo Server

This script demonstrates how to properly communicate with an MCP server
by sending valid JSON-RPC messages.
"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_echo_server():
    """Test the echo server by calling the echo tool."""
    print("Starting MCP Echo Server test client...", file=sys.stderr)
    print("-" * 50, file=sys.stderr)

    # Start the server as a subprocess
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✓ Connected to server", file=sys.stderr)

                # List available tools
                tools = await session.list_tools()
                print(f"✓ Available tools: {[tool.name for tool in tools.tools]}", file=sys.stderr)

                # Test the echo tool with different messages
                test_messages = [
                    "Hello, MCP Server!",
                    "echo",
                    "fdfdfdfdf",
                    "This is a properly formatted JSON-RPC request!"
                ]

                for msg in test_messages:
                    print(f"\n→ Sending: '{msg}'", file=sys.stderr)
                    result = await session.call_tool("echo", {"message": msg})

                    for content in result.content:
                        print(f"← Received: {content.text}", file=sys.stderr)

                print("\n" + "-" * 50, file=sys.stderr)
                print("✓ All tests completed successfully!", file=sys.stderr)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        raise


async def interactive_mode():
    """Run an interactive session with the echo server."""
    print("Starting interactive MCP Echo Server session...", file=sys.stderr)
    print("Type your messages (Ctrl+C or 'quit' to exit)", file=sys.stderr)
    print("-" * 50, file=sys.stderr)

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✓ Connected to server\n", file=sys.stderr)

                while True:
                    try:
                        message = input("You: ")
                        if message.lower() in ['quit', 'exit', 'q']:
                            break

                        result = await session.call_tool("echo", {"message": message})

                        for content in result.content:
                            print(f"Server: {content.text}")

                    except EOFError:
                        break
                    except KeyboardInterrupt:
                        print("\nExiting...", file=sys.stderr)
                        break

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        raise


async def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_mode()
    else:
        await test_echo_server()


if __name__ == "__main__":
    asyncio.run(main())
