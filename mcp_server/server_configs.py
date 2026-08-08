from datetime import datetime

from fastmcp import Context

from configurations.config import base_dir, get_realtive_path
from mcp_server.server import server
from schema.document import DocumentGeneratorSchema


@server.tool()
async def write_file(file_path:str,content:str, ctx:Context):
    
    """
    Create or overwrite a file with the provided content.

    The parent directories are created automatically if they don't exist.
    The file is written using UTF-8 encoding.
    """
    
    
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
    
    
@server.tool()
async def delete_file(file_path:str, ctx:Context):
    
    """
    Delete a file from a given file path.
    check whether the path is a file or directory.
    
    if path is a file then delete it.
    if path is a directory returns a warning.
       
    """
    
    try:
        
        path = get_realtive_path(file_path)

        if not path.exists():
            raise ValueError(f"Path is not exists: {path}")
        
        if path.is_file():
            path.unlink()
            await ctx.info(f"Successfully remove file from path: {file_path}")
            return f"Successfully remove file from path: {file_path}"
        
        elif path.is_dir():
            await ctx.warning(f"Warning, path is a directory not a file: {file_path}")
            return f"Warning, path is a directory not a file: {file_path}"
        
        else:
            await ctx.warning(f"File not found in: {file_path}")
            return f"File not found in: {file_path}"
        
                
    except Exception as e:
        await ctx.error(f"Error in delete file: {e}")
        raise
    
@server.resource("file:///{file_name}")  
async def read_file_from_resources(file_name:str, ctx:Context) -> dict:
    
    """read a file from mcp server resources. this function provides operation to access a paticular file
    using its path to retrieve its content

    Returns:
        _type_: _description_
    """
    
    try:
        
        path = get_realtive_path(file_name)
        
        if not (path.exists or path.is_file):
            await ctx.warning(f"Error: file is not exists or path is not a file: {file_name}")
            return{
                "error": f"Error: file is not exists or path is not a file: {file_name}"
            }
            
        await ctx.info(f"file fetched: {file_name}")
        return {
            "file_content": path.read_text(encoding="utf-8")
        }
        
    except Exception as e:
        await ctx.error(f"Error in read file: {e}")
        raise
    
@server.resource("dir://.")    
async def read_root_dir(ctx:Context):
    
    try:
        path = get_realtive_path(".")
        
        if not path.exists():
            await ctx.warning("error: root path does not exists")
            return {
                "error": "root path does not exists"
            }
        
        items = []
        
        for item in path.iterdir():
            
            status = item.stat()
            
            items.append({
                "name": item.name,
                "path": str(item.relative_to(base_dir)),
                "type": "file" if item.is_file() else "directory",
                "size": status.st_size,
                "created": datetime.fromtimestamp(status.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(status.st_mtime).isoformat()
            })
            
        await ctx.info("root directory read successful")
        return {
            "items": items
        }
        
    except Exception as e:
        await ctx.error(f"Error in read root dir: {e}")
        raise
    
    
@server.prompt()
async def document_generator(ctx:Context):
    
    """ Generate documentation according to the given code documentation.
        
        Reads a code file, elicits a documentation filename from the user,
        and generate prompt to feed to the chat groq agent to create a comprehensive documentation.
    """
    
    try:
        
        result = await ctx.elicit(
            message="Please give the file path and file name",
            response_type=DocumentGeneratorSchema
        )
        
        file_path = result.data.file_path
        path = get_realtive_path(file_path)
        file_name = result.data.file_name
        
        code = path.read_text(encoding="utf-8")
        language = path.suffix.lower()
        
        if not path.exists() or not path.is_file():
            await ctx.warning(f"file not found: {file_path}")
            return f"file not found: {file_path}"
        
        prompt =f"""You are an expert technical writer and documentation specialist. Create documentation for the following code file:

                File: {file_path}
                Language (file suffix): {language or "unknown"}

                Current code:
                '''
                {code}
                '''

                Use MCP tools available to you to create the separate documentation file:
                - **CRITICAL DETAIL: Name that separate document EXACTLY: {file_name}**
                - Add the .md suffix yourself if the name doesn't include it already
            """
            
        await ctx.info("Prompt is configured")
        return prompt
        
        
    except Exception as e:
        await ctx.error(f"Error in document generator: {e}")
        raise
        
