
from contextlib import AsyncExitStack

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.stdio import StdioServerParameters, stdio_client 
from mcp import ClientSession
from mcp.types import ElicitResult

from agents.llm_agent import LLMAgent
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
        
    async def elicitation_handler(self, params):
        
        try:
            logger.info(f"Server message: {params.message}")
            
            schema = params.requestedSchema
            
            user_response = {}
            
            for field_name, field_schema in schema['properties'].items():
                value = input(f"{field_name}: ")
                
                if value is None:
                    return ElicitResult(
                        action="decline"
                    )
                    
                user_response[field_name] = value
            
            logger.info(f"Elicitation response: {user_response}")
            
            return ElicitResult(
                action="accept",
                content=user_response
            )
            
        except Exception as e:
            logger.error(f"error in elicitation handler: {e}")
            raise
        
    async def init_agent(self):
        
        try:
            if self.agent is not None:
                raise RuntimeError("Agent already initialized")
            
            if self.session is None:
                raise RuntimeError("Client session is not initialized")
            
            tools = await load_mcp_tools(self.session)
            logger.info("Tools extracted successful")
            self.agent = LLMAgent(tools=tools)
            logger.info("Agent run")
            
        except Exception as e:
            logger.error(f"Error in init agent: {e}")
            raise