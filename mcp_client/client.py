
from contextlib import AsyncExitStack

from mcp.client.stdio import StdioServerParameters, stdio_client 
from mcp import ClientSession

from configurations.logger import get_logger


logger = get_logger("mcp_client")

class MCPClient:
    
    def __init__(self):
        
        try:
            
            self.agent = None
            self.session = None
            self.server_params = None
            self.exit_stack = AsyncExitStack()
            
        except Exception as e:
            logger.error(f"Error in mcp clinet initialization: {e}")
            raise
        
    
    async def connect_to_server(self, server_script_path:str):
        
        try:
                
            if self.session is not None:
                raise RuntimeError(
                    "MCP client session already up!!!"
                )
                
            if not server_script_path:
                raise ValueError("Server script is missing")
            
            
            if server_script_path.endswith((".js", ".py", ".ts")):
                
                self.server_params = StdioServerParameters(
                    command="python",
                    args=["-m", server_script_path]
                )
            
            elif "." in server_script_path:
                
                self.server_params = StdioServerParameters(
                    command="python",
                    args=[server_script_path]
                )
            
            else:
                raise ValueError("server script should be a .js, .ts, or .py file")
                
            logger.info("server script fetched success")
            
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(self.server_params)
            )
            
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(
                    read, 
                    write,
                    client_info={
                        "name": "enhanced-mcp-client",
                        "version": "1.0.0"
                    },
                    elicitation_callback = self.elicitation_handler
                )  
            )
            
            await self.session.initialize()
            logger.info("Client session is created")
 
        except ValueError as e:
            logger.error(f"Value error in server connection: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in connect to server: {e}")
            raise