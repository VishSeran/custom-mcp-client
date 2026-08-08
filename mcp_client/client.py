
from contextlib import AsyncExitStack

from mcp.client.stdio import StdioServerParameters, stdio_client 
from mcp import ClientSession

from configurations.logger import get_logger


logger = get_logger("mcp_client")

class MCPClient:
    
    def __init__(self):
        
        try:
            
            self.agent = None
            self.client = None
            self.session = None
            self.exit_stack = AsyncExitStack()
            
        except Exception as e:
            logger.error(f"Error in mcp clinet initialization: {e}")
            raise
        
    
    async def connect_to_server(self, server_script_path:str):
        
        try:
            
            if self.client is not None:
                raise RuntimeError(
                    "MCP Client Already Up!!!"
                )
                
            if self.session is not None:
                raise RuntimeError(
                    "MCP client session already up!!!"
                )
                
            if not server_script_path:
                raise ValueError("Server script is missing")
            
            
            
            
            
                
            
        except ValueError as e:
            logger.error(f"Value error in server connection: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in connect to server: {e}")
            raise