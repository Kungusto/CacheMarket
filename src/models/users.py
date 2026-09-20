from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class UsersORM(BaseORM):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]