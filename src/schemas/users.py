from pydantic import BaseModel


class UserAddDTO(BaseModel):
    email: str
    hashed_password: str

class UserDTO(UserAddDTO):
    user_id: int
