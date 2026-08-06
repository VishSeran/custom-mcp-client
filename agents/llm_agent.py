import os
import dotenv


from configurations.logger import get_logger
from configurations.config import MODEL_NAME

dotenv.load_dotenv()


logger = get_logger("llm-agent")

class LLMAgent:
    
    def __init__(self, model_name=MODEL_NAME):
        
        
        try:
            
            groq_api = os.getenv("groq_api")
            
            if groq_api is None:
                raise ValueError ("Groq key is missing")
            
        except ValueError as e:
            logger.error(f"Value Error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in get realtive path: {e}")
            raise