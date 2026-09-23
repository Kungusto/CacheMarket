from typing import ClassVar

from src.utils.db_manager import DBManager


class AnswersConfig:
    OK_ANSWER: ClassVar[dict] = {"status": "OK"}


class BaseService:
    def __init__(self, db: DBManager):
        self.db = db

        self.answers = AnswersConfig()
