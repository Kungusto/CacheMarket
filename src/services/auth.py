import copy
import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from src.config import settings


class PasswordService:
    pwd_hash = PasswordHash.recommended()

    @classmethod
    def hash_password(cls, pwd: str) -> str:
        return cls.pwd_hash.hash(pwd)

    @classmethod
    def verify_password(cls, pwd_to_check: str, hashed_pwd: str) -> bool:
        return cls.pwd_hash.verify(pwd_to_check, hashed_pwd)


class AccessTokenService:
    @classmethod
    def encode_token(cls, payload: dict[Any, Any]):
        to_encode = copy.copy(payload)
        iat = datetime.now(timezone.utc)
        exp_minutes = settings.jwt.ACCESS_TOKEN_EXP
        exp = iat + timedelta(seconds=exp_minutes)
        to_encode.update({"iat": iat, "exp": exp})
        return jwt.encode(
            payload=to_encode,
            key=settings.jwt.PRIVATE_KEY_PATH.read_text(),
            algorithm=settings.JWT_ALGORITHM
        )

    @classmethod
    def decode_token(cls, token: str) -> dict[Any, Any]:
        return jwt.decode(
            jwt=token,
            key=settings.jwt.PUBLIC_KEY_PATH,
            algorithms=[settings.JWT_ALGORITHM]
        )

class RefreshTokenService:
    LENGTH: int = 128

    @classmethod
    def get_refresh_token(cls) -> str:
        return secrets.token_hex(cls.LENGTH // 2)

    @staticmethod
    def hash_token(token: str):
        return hashlib.sha256(token.encode()).hexdigest()