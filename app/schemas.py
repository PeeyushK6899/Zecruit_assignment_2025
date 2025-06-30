from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str

class JobOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True