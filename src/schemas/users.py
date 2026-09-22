from src.schemas.mixins.users import UserPrivateInfoMixin, UserPublicInfoMixin


class UserAddDTO(UserPrivateInfoMixin, UserPublicInfoMixin):
    pass

class UserDTO(UserAddDTO):
    user_id: int

class UserPublicSchema(UserPublicInfoMixin):
    user_id: int
