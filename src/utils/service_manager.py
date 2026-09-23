from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class ServiceManager:
    def __init__(self, db: DBManager):
        self.auth = AuthService(db=db)
