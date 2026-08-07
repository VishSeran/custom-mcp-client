from pydantic import BaseModel


class DocumentGenerator(BaseModel):
    
    file_path: str
    file_name: str
    
    


