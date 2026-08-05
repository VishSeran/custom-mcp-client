# Build a Custom MCP Client with Python

A minimal, from-scratch Python implementation of a **Model Context Protocol (MCP)** client and server, built to demonstrate the core MCP primitives — tools, resources, and prompts — over STDIO transport.

## Overview

This project walks through building:

- A **FastMCP server** (`mcp_server.py`) exposing:
  - An `echo` tool
  - A `write_file` tool
  - A `file://resources/{filename}` resource template
  - A `review_file` prompt template
- A **lightweight MCP client** (`mcp_client.py`) that connects to the server via STDIO transport and provides an interactive command-line interface for discovering and invoking tools, reading resources, and rendering prompts.

By the end, you'll have a working client/server pair you can extend for your own MCP-based applications.

## Learning Objectives

After working through this project, you will be able to:

- Connect to an MCP server using STDIO transport
- Discover and invoke MCP tools
- Read MCP resources via URIs
- Execute MCP prompt templates
- Handle MCP protocol sessions properly

## Prerequisites

- Basic Python programming knowledge
- Understanding of MCP architecture (client-server model)
- Familiarity with async/await patterns in Python
- Awareness of MCP concepts: tools, resources, and prompts

## Project Structure

```
mcp_client_lab/
├── mcp_server.py       # FastMCP server exposing tools, resources, and prompts
├── mcp_client.py        # STDIO-based MCP client with a CLI
└── resources/
    ├── project_info.txt
    ├── README.md
    └── notes.txt
```

## Setup

### 1. Create a virtual environment

```bash
python3.11 -m venv mcp_client_env
source mcp_client_env/bin/activate
```

### 2. Install dependencies

```bash
pip install mcp==1.16.0 fastmcp==2.12.5
```

### 3. Create the project structure

```bash
mkdir mcp_client_lab
cd mcp_client_lab
mkdir resources
```

## Usage

Run the client, pointing it at the server script:

```bash
python mcp_client.py mcp_server.py
```

You should see:

```
✓ Connected to MCP server

=== MCP Client ===
Commands: tools | call | resources | read | prompts | prompt | quit
>
```

### Available Commands

| Command     | Description                              |
|-------------|-------------------------------------------|
| `tools`     | List available tools                      |
| `call`      | Invoke a tool with JSON arguments          |
| `resources` | List resource templates                    |
| `read`      | Read a resource by URI                      |
| `prompts`   | List prompt templates                       |
| `prompt`    | Get a rendered prompt with JSON arguments   |
| `quit`      | Exit the client                             |

### Example Session

```
> tools
 • echo: Echo back the input text.
 • write_file: Write content to a file.

> call
 Tool name: echo
 Arguments (as JSON, for example, {"text": "hello"}): {"text": "Hello MCP!"}
 Result: Echo: Hello MCP!

> resources
 • read_resource_file
   URI template: file://resources/{filename}

> read
 URI: file://resources/README.md
[... file contents ...]

> prompts
 • review_file: Generate a prompt to review a file's contents. (args: filename)

> prompt
 Prompt name: review_file
 Arguments (as JSON): {"filename": "test.txt"}
[... rendered prompt ...]
```

## Key Concepts

- **STDIO Transport** — Local communication via stdin/stdout; simple, low-latency, and ideal for development.
- **ClientSession** — Manages MCP protocol details (JSON-RPC, message IDs, initialization handshake, etc.).
- **FastMCP** — Simplifies server creation with decorators (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`) and automatic JSON schema generation from Python type hints.
- **Tools** — Server-side actions the client can invoke with arguments (e.g., `echo`, `write_file`).
- **Resource Templates** — URI patterns such as `file://resources/{filename}` that dynamically expose multiple resources without defining each individually.
- **Prompts** — Server-defined templates that render structured, parameterized messages for use with an LLM.

## Architecture

### Connection Flow

```
1. Launch client with server script path
   ↓
2. Create StdioServerParameters
   ↓
3. Launch server as subprocess via stdio_client
   ↓
4. Create ClientSession with read/write streams
   ↓
5. Call session.initialize() (MCP handshake)
   ↓
6. Ready for operations
```

### Resource Reading Flow

```
User provides URI (e.g., "file://resources/README.md")
   ↓
Client calls session.read_resource(uri)
   ↓
[JSON-RPC request sent via stdin]
   ↓
Server matches URI to template pattern "file://resources/{filename}"
   ↓
Server extracts parameter: filename = "README.md"
   ↓
Server calls read_resource_file("README.md")
   ↓
[JSON-RPC response sent via stdout]
   ↓
Client receives and displays the result
```

## Extending the Client

Some ideas for extending this project:

- **History log** — Track a running log of tool calls and other operations.
- **Better error messages** — Add friendlier hints for common errors (invalid JSON, resource not found, etc.).
- **Help command** — Add a `help` command that lists all available commands and their descriptions.

## Best Practices

1. **Always use `AsyncExitStack`** to ensure proper cleanup, even when errors occur.
2. **Initialize before operations** — always call `await session.initialize()` after creating the session.
3. **Handle JSON parsing errors** gracefully when accepting user input.
4. **Understand resource templates** — discover them via `list_resource_templates()`, then substitute concrete values to build valid URIs.
5. **Inspect tool schemas** from `list_tools()` to understand required/optional arguments before calling.
6. **Validate URIs** against available templates before reading resources.
7. **Close cleanly** — always run cleanup in a `finally` block.

## License

The content of this project is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).
