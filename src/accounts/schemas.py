from pydantic import BaseModel, Field,EmailStr

class UserBase(BaseModel):
    username : str
    email : EmailStr
    full_name : str

class UserCreate(UserBase):
    password : str = Field(..., min_length=8, max_length=20)



class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True