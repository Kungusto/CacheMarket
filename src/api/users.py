from fastapi import APIRouter, Response, Request
from icecream import ic

from src.api.dependencies import ServiceDep, UserIdDep
from src.schemas.auth import AuthUserSchema

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