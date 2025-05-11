from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username : str
    email : str
    full_name : str

class UserCreate(UserBase):
    password : str = Field(..., min_length=8, max_length=20)



class UserRead(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True