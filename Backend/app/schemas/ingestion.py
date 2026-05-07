from pydantic import BaseModel

class IngestionCreate(BaseModel):
    source: str

class IngestionResponse(BaseModel):
    id: int
    status: str
    source: str

    class Config:
        from_attributes = True