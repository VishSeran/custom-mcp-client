
from fastmcp import FastMCP

from configurations.logger import get_logger


logger = get_logger("server")

class MCPServer:
    
    def __init__(self):
        
        try:
            
            self.mcp_server = FastMCP(
                name="FileMCPServer",
                instructions="""
                This server facilitates different tools, resources and prompts that support for 
                file operations."""
            )
            logger.info("MCP server has initialized")
            
        except Exception:
            logger.exception("Failed to initialized the MCp server")
            raise
        

mcp = MCPServer()
server = mcp.mcp_server