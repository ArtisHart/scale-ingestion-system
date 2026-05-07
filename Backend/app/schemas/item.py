from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    value: int

class ItemResponse(BaseModel):
    id: int
    name: str
    value: int

    class Config:
        from_attributes = True