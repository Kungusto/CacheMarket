from src.exceptions.base import BaseAppException


class DatabaseException(BaseAppException):
    message = "Непредвиденная ошибка на стороне БД"


class EntityAlreadyExists(DatabaseException):
    message = "Эта сущность уже существует"
