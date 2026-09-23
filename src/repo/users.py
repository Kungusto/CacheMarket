from src.decorators.cache import cache
from src.models.users import UsersORM
from src.repo.base import BaseRepo
from src.schemas.users import UserDTO


class UsersRepo(BaseRepo):
    schema = UserDTO
    model = UsersORM

    @cache(ttl=30, key_format="user:email:{email}")
    async def get_user_by_email(self, email: str) -> UserDTO:
        return await super().get_filtered(
            self.model.email == email,
            get_one=True,
        )

    @cache(ttl=120, key_format="user:id:{user_id}")
    async def get_user_by_user_id(self, user_id: int) -> UserDTO:
        return await super().get_filtered(
            self.model.user_id == user_id,
            get_one=True,
        )
