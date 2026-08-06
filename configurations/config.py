from configurations.logger import get_logger


MODEL_NAME = "llama-3.3-70b-versatile"

logger = get_logger("config")

def get_realtive_path(path:str):
    
    try:
        
    except ValueError as e:
        logger.error(f"Value Error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Error in get realtive path: {e}")
        raise
        
