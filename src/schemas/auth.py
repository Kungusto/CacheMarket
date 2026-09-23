from pydantic import BaseModel, EmailStr


class AuthUserSchema(BaseModel):
    email: EmailStr
    password: str
