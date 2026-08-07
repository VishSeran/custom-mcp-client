from fastmcp import Context

from mcp_server.server import server

from configurations.config import get_realtive_path

@server.tool()
async def write_file(file_path:str,content:str, ctx:Context):
    
    
    try:
        path = get_realtive_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        total_size = len(content)
        chunk_size = max(total_size //10, 1)
        
        written = 0
        
        with open(path, "w", encoding="utf-8") as f:
            for i in range(0, total_size, chunk_size):
                f.write(content[i:i+chunk_size])
                written = min(i+chunk_size, total_size)
                
                await ctx.report_progress(progress=written, total=total_size,
                                          message=f'Written progress: {written}/{total_size}')
        
        await ctx.report_progress(
            progress=written,
            total= total_size,
            message="Written is completed"
        ) 
        return f"Content is written to file path: {file_path}"
        
    except Exception as e:
        await ctx.error(f"Error in write file: {e}")
        raise
    