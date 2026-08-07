from fastmcp import Context

from mcp_server.server import server

@server.tool()
async def write_file(file_path:str,content:str, ctx:Context):
    
    
    try:
        
        
        
    except Exception as e:
        await ctx.error(f"Error in write file: {e}")
        raise
    