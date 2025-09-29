from pydantic import BaseModel, EmailStr, constr

class UserCreateSchema(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)
    role: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
