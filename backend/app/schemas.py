from pydantic import BaseModel, EmailStr
from datetime import datetime



class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str    



class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    updated_at: datetime
    class Config:
        from_attributes = True

