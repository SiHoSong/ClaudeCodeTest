# Simple MCP Echo Server

A minimal MCP (Model Context Protocol) server in Python that echoes back any input.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Important Note

This MCP server communicates using JSON-RPC messages over stdin/stdout. **You cannot simply type plain text into the terminal** when running the server directly - this will cause validation errors.

### Testing the Server

Use the provided test client:

```bash
# Run automated tests
python test_client.py

# Run in interactive mode
python test_client.py --interactive
```

### Running with an MCP Client

The server is designed to be used with MCP-compatible clients (like Claude Desktop, IDEs with MCP support, etc.). Add it to your client configuration as shown below.

## Features

The server provides one tool:
- **echo**: Takes a message and echoes it back

## MCP Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "echo": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## Example

When you call the `echo` tool with `{"message": "Hello World"}`, it returns:
```
Echo: Hello World
``` 
