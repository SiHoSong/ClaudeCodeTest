# Simple MCP Echo Server

A minimal MCP (Model Context Protocol) server in Python that echoes back any input.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the server:

```bash
python server.py
```

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
