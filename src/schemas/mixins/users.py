from pydantic import BaseModel


class UserPublicInfoMixin(BaseModel):
    email: str


class UserPrivateInfoMixin(BaseModel):
    hashed_password: str
