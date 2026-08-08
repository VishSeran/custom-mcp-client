
from contextlib import AsyncExitStack

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