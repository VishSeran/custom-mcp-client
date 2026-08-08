from pydantic import BaseModel


class DocumentGeneratorSchema(BaseModel):
    
    file_path: str
    file_name: str
    
    


