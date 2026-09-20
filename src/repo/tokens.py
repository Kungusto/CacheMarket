from src.models import RefreshTokensORM
from src.repo.base import BaseRepo
from src.schemas.tokens import RefreshTokenDTO


class RefreshTokensRepo(BaseRepo):
    model = RefreshTokensORM
    schema = RefreshTokenDTO
