from datetime import datetime, timezone, timedelta

from fastapi import Response, Request
from icecream import ic
from starlette.responses import Response

from src.exceptions.auth import AlreadyLoggedInHTTPException
from src.services.base import BaseService
from src.config import settings
from src.exceptions.db import DatabaseException
from src.exceptions.users import EmailAlreadyRegisteredHTTPException, UserNotFoundHTTPException, \
    WrongPasswordHTTPException
from src.schemas.auth import AuthUserSchema
from src.schemas.tokens import RefreshTokenAddDTO
from src.schemas.users import UserAddDTO, UserDTO, UserPublicSchema
from src.services.auth import PasswordService, AccessTokenService, RefreshTokenService


class UsersService(BaseService):
    async def _auth_user(self, response_inst: Response, user_id: int):
        access_token = AccessTokenService.encode_token(
            payload={"user_id": str(user_id)}
        )
        refresh_token = RefreshTokenService.get_refresh_token()
        hashed_refresh_token = RefreshTokenService.hash_token(token=refresh_token)
        await self.db.refresh_tokens.add(
            data=RefreshTokenAddDTO(
                token_hash=hashed_refresh_token,
                user_id=user_id,
                created_at=datetime.now(timezone.utc),
                expires_at=datetime.now(timezone.utc) + timedelta(
                    seconds=settings.jwt.REFRESH_TOKEN_EXP
                )
            )
        )
        response_inst.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.jwt.ACCESS_TOKEN_EXP
        )
        response_inst.set_cookie(
            key="refresh_token",
            value=refresh_token,
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=settings.jwt.REFRESH_TOKEN_EXP
        )

    async def register_user(self, data: AuthUserSchema, response_inst: Response):
        hashed_pwd = PasswordService.hash_password(pwd=data.password)
        try:
            user: UserDTO = await self.db.users.add(
                data=UserAddDTO(
                    email=data.email,
                    hashed_password=hashed_pwd
                )
            )
        except DatabaseException as ex:
            raise EmailAlreadyRegisteredHTTPException from ex
        await self._auth_user(response_inst, user.user_id)
        await self.db.commit()
        return {
            "user": {
                "user_id": user.user_id,
                "email": user.email,
            },
            "status": "OK"
        }

    async def login_user(self, data: AuthUserSchema, request: Request, response_inst: Response):
        cookies = request.cookies
        access_token = cookies.get("access_token", None)
        if access_token is not None:
            raise AlreadyLoggedInHTTPException()
        user: UserDTO = await self.db.users.get_user_by_email(email=data.email)
        if user is None:
            raise UserNotFoundHTTPException()
        verify_pwd = PasswordService.verify_password(
            hashed_pwd=user.hashed_password,
            pwd_to_check=data.password
        )
        if not verify_pwd:
            raise WrongPasswordHTTPException()
        await self._auth_user(response_inst, user.user_id)
        return {"status": "OK"}


    async def get_curr_user(self, user_id: int):
        user = await self.db.users.get_user_by_user_id(user_id=user_id)
        return UserPublicSchema.model_validate(user, from_attributes=True)