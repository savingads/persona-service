# Persona Service Integration Guide

This guide explains how to integrate the Persona Service into your applications.

## REST API Integration

You can make direct HTTP requests to the Persona Service API endpoints.

```python
import requests

def get_personas(base_url="http://localhost:5050"):
    response = requests.get(f"{base_url}/api/v1/personas")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get personas: {response.text}")
```

## Python Client Library

For Python applications, you can use the persona-client library:

```python
from personaclient import PersonaClient

client = PersonaClient(base_url="http://localhost:5050", api_version="v1")
personas = client.get_all_personas()
```

## MCP Integration

For AI assistant integration, you can create an MCP server that connects to the Persona Service:

1. Create an MCP server that implements the MCP protocol
2. Create tools and resources that fetch data from the Persona Service
3. Use the MCP server to provide persona context to AI assistants

An example MCP server implementation is provided in the `examples/mcp-server` directory.
