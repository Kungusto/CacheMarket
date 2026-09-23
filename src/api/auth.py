from fastapi import APIRouter, Request, Response

from src.api.dependencies import RefreshTokenDep, ServiceDep, UserIdDep
from src.schemas.auth import AuthUserSchema
from src.schemas.requests.auth import RefreshTokenHashToRevoke

router = APIRouter(prefix="/auth", tags=["👥 Пользователи"])


@router.post(path="/register")
async def register_user(data: AuthUserSchema, response: Response, service: ServiceDep):
    return await service.auth.register_user(data=data, response_inst=response)


@router.post(path="/login")
async def login_user(
    data: AuthUserSchema, service: ServiceDep, request: Request, response_inst: Response
):
    return await service.auth.login_user(
        data=data, request=request, response_inst=response_inst
    )


@router.get(path="/me")
async def get_user_data(
    service: ServiceDep,
    user_id: UserIdDep,
):
    return await service.auth.get_curr_user(user_id=user_id)


@router.get(path="/sessions")
async def get_all_sessions(
    service: ServiceDep,
    user_id: UserIdDep,
):
    return await service.auth.get_user_sessions(user_id=user_id)


@router.post(path="/logout")
async def logout_session(service: ServiceDep, request: Request, response: Response):
    return await service.auth.logout_session(
        request=request,
        response=response,
    )


@router.post(path="/refresh")
async def update_refresh_token(
    service: ServiceDep,
    refresh_token: RefreshTokenDep,
    user_id: UserIdDep,
    response: Response,
):
    return await service.auth.update_refresh_token(
        curr_token=refresh_token, user_id=user_id, response=response
    )


@router.post(path="/sessions/revoke")
async def revoke_session(
    data: RefreshTokenHashToRevoke,
    service: ServiceDep,
):
    return await service.auth.revoke_session(data=data)
