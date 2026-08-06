from pathlib import Path

from configurations.logger import get_logger


MODEL_NAME = "llama-3.3-70b-versatile"
base_dir = Path.cwd().resolve()

logger = get_logger("config")

def get_realtive_path(path:str):
    
    try:
        if path is None:
            raise ValueError("path is missing")
        
        file_path = (base_dir/path).resolve()
        file_path.relative_to(base_dir)
        
        return file_path
        
    except ValueError as e:
        logger.error(f"Value Error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Error in get realtive path: {e}")
        raise
        
