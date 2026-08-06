import os
import dotenv

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from configurations.logger import get_logger
from configurations.config import MODEL_NAME

dotenv.load_dotenv()


logger = get_logger("llm-agent")

class LLMAgent:
    
    def __init__(self, tools,model_name=MODEL_NAME):
        
        
        try:
            
            groq_api = os.getenv("groq_api")
            
            if groq_api is None:
                raise ValueError ("Groq key is missing")
            
            if model_name is None:
                raise ValueError ("Groq key is missing")
            
            if groq_api is None:
                raise ValueError ("Groq key is missing")
            
            chat_groq = ChatGroq(
                model=model_name,
                api_key=groq_api,
                temperature=0.4,
                max_tokens=5000,
                model_kwargs={
                    "parallel_tool_calls": False
                }
            )
            
            logger.info("Chat groq initiated")
            
            checkpointer = InMemorySaver()
            
            self.configs = {
                "configurable": {
                    "thread_id": "conversatioanl_id"
                }
            }
            
            self.agent
                        
        except ValueError as e:
            logger.error(f"Value Error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in get realtive path: {e}")
            raise