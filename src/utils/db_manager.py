from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.repo.products import ProductsRepo
from src.repo.tokens import RefreshTokensRepo
from src.repo.users import UsersRepo


class DBManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.products = ProductsRepo(session=self.session)
        self.users = UsersRepo(session=self.session)
        self.refresh_tokens = RefreshTokensRepo(session=self.session)

        return self

    async def __aexit__(self, *exc):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()