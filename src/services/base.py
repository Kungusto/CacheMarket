from src.utils.db_manager import DBManager


class BaseService:
    def __init__(self, db: DBManager):
        self.db = db
