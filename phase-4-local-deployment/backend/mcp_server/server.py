from mcp.server import Server
from .tools.task_operations import register_tools
import asyncio
import os
from ..config import settings


def create_mcp_server():
    """Create and configure the MCP server"""
    server = Server(
        name="todo-mcp-server",
        # Add description and other metadata
    )

    # Register all tools
    register_tools(server)

    return server


async def run_mcp_server():
    """Run the MCP server"""
    server = create_mcp_server()

    # Run the server
    await server.run()


if __name__ == "__main__":
    asyncio.run(run_mcp_server())