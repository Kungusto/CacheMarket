from sqlalchemy import select

from src.decorators.cache import cache
from src.models.users import UsersORM
from src.repo.base import BaseRepo
from src.schemas.users import UserDTO


class UsersRepo(BaseRepo):
    schema = UserDTO
    model = UsersORM

    @cache(ttl=30, key_format="user:email:{email}")
    async def get_user_by_email(self, email: str):
        return await super().get_filtered(
            self.model.email == email,
            get_one=True,
        )
