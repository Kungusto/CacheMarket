from fastapi import APIRouter, Response, Request
from icecream import ic


from src.api.dependencies import ServiceDep, UserIdDep
from src.exceptions.auth import UnauthorizedHTTPException
from src.schemas.auth import AuthUserSchema
from src.services.auth import RefreshTokenService

router = APIRouter(prefix="/auth", tags=["👥 Пользователи"])

@router.post(
    path="/register"
)
async def register_user(
    data: AuthUserSchema,
    response: Response,
    service: ServiceDep
):
    return await service.users.register_user(data=data, response_inst=response)


@router.post(
    path="/login"
)
async def login_user(
    data: AuthUserSchema,
    service: ServiceDep,
    request: Request,
    response_inst: Response
):
    return await service.users.login_user(
        data=data,
        request=request,
        response_inst=response_inst
    )


@router.get(
    path="/me"
)
async def get_user_data(
    service: ServiceDep,
    user_id: UserIdDep,
):
    return await service.users.get_curr_user(user_id=user_id)

@router.get(
    path="/sessions"
)
async def get_all_sessions(
    service: ServiceDep,
    user_id: UserIdDep,
):
    return await service.sessions.get_user_sessions(user_id=user_id)


@router.post(
    path="/logout"
)
async def logout_session(
    service: ServiceDep,
    request: Request,
    response: Response
):
    return await service.sessions.logout_session(
        request=request,
        response=response,
    )