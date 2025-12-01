# MCP Servers

This directory contains Model Context Protocol (MCP) server implementations for Ask PanDA.

## Overview

MCP servers provide a standardized way to expose Ask PanDA functionality to AI assistants and tools.

## Available Servers

- `panda_server.py` - Main MCP server for PanDA queries
- `docs_server.py` - MCP server for documentation search

## Usage

### Running the PanDA Server

```bash
python -m mcp.panda_server
```

### Running the Documentation Server

```bash
python -m mcp.docs_server
```

## Configuration

Set the following environment variables:

- `EXPERIMENT` - Default experiment (atlas, verarubin, epic)
- `OPENAI_API_KEY` - OpenAI API key for LLM queries
- `MODEL_NAME` - Model to use (default: gpt-4)

## Integration

These servers can be used with MCP-compatible clients to provide PanDA querying capabilities.
