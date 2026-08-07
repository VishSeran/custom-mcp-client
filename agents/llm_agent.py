import os
import dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent
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
            
            self.agent = create_agent(
                model=chat_groq,
                tools=tools,
                checkpointer=checkpointer,
                system_prompt="""
                            You are a useful AI agent.
                            You have access to the tools that provided.
                            Use the relevant tools if needed when answering the user questions.
                """
            )
            
            logger.info("LLM Agent initiated!!!")
                        
        except ValueError as e:
            logger.error(f"Value Error in llm agent: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in llm agent initialization: {e}")
            raise
        
        
    async def get_response(self, query):
        
        try:
            
            if query is None:
                raise ValueError("Query is missing")
            
            response =  await self.agent.ainvoke({
                "messages":[{
                    "role": "user",
                    "content": query
                }]
            })
            
            result = response['messages'][-1].content
            logger.info("Response has fetched successs")
            
            return result
        
        
        except ValueError as e:
            logger.error(f"Value Error in get response: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in llm get response: {e}")
            raise
                