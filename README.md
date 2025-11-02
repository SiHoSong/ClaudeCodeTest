# Simple MCP Echo Server

A minimal MCP (Model Context Protocol) server in Python that echoes back any input.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### server.py Overview

`server.py` is an MCP server that implements the Model Context Protocol to communicate with MCP-compatible clients (like Claude Desktop). It provides a simple "echo" tool that returns whatever message you send to it.

**Important:** This server communicates using JSON-RPC messages over stdin/stdout. **You cannot simply type plain text into the terminal** when running the server directly - this will cause validation errors.

### Running the Server

#### Option 1: Testing with test_client.py (Recommended for Development)

Use the provided test client to verify the server works correctly:

```bash
# Run automated tests
python test_client.py

# Run in interactive mode (chat with the server)
python test_client.py --interactive
```

The test client handles all the JSON-RPC communication for you and provides a simple interface to test the echo functionality.

#### Option 2: Running Standalone (Not Recommended)

You can run the server directly, but it will wait for JSON-RPC formatted input:

```bash
python server.py
```

This mode is only useful when the server is being controlled by an MCP client like Claude Desktop.

### Connecting to Claude Desktop

To use this server with Claude Desktop, you need to configure it in Claude's MCP settings.

#### Step 1: Locate the Claude Desktop Configuration File

The configuration file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Step 2: Edit the Configuration File

Open the configuration file in a text editor and add the server configuration:

```json
{
  "mcpServers": {
    "echo-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

**Important:** Replace `/absolute/path/to/server.py` with the actual absolute path to your `server.py` file.

For example:
- macOS/Linux: `"/home/user/ClaudeCodeTest/server.py"`
- Windows: `"C:\\Users\\YourName\\ClaudeCodeTest\\server.py"`

#### Step 3: Restart Claude Desktop

After saving the configuration file, completely quit and restart Claude Desktop for the changes to take effect.

#### Step 4: Verify the Connection

Once Claude Desktop restarts:
1. Open a new conversation
2. Look for the MCP tools icon (usually a hammer or tool icon)
3. You should see the "echo" tool available
4. Try using it by asking Claude: "Use the echo tool to repeat 'Hello World'"

### Example Configuration for Different Environments

#### Using Python Virtual Environment

If you're using a virtual environment:

```json
{
  "mcpServers": {
    "echo-server": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

#### Using Python 3 Explicitly

```json
{
  "mcpServers": {
    "echo-server": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

## Features

The server provides one tool:
- **echo**: Takes a message and echoes it back

### Tool Schema

```json
{
  "name": "echo",
  "description": "Echoes back the input text you provide",
  "inputSchema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The message to echo back"
      }
    },
    "required": ["message"]
  }
}
```

## Example Usage

When you call the `echo` tool with `{"message": "Hello World"}`, it returns:
```
Echo: Hello World
```

In Claude Desktop, you can simply ask:
- "Use the echo tool to say hello"
- "Echo this message: Testing 123"
- "Can you use the echo tool with 'MCP is working!'"

## Troubleshooting

### Server Not Appearing in Claude Desktop

1. Check that the path to `server.py` is absolute, not relative
2. Verify Python is in your PATH or use the full path to Python
3. Make sure you completely quit and restarted Claude Desktop
4. Check the Claude Desktop logs for error messages

### JSON Validation Errors

If you see validation errors when testing:
- Use `test_client.py` instead of running `server.py` directly
- The server expects JSON-RPC formatted messages, not plain text

### Dependencies Not Found

Make sure you've installed the required packages:
```bash
pip install -r requirements.txt
```

Or install the MCP SDK directly:
```bash
pip install mcp
``` 
