from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Form
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from authentication.utils import get_current_user, http_bearer
from core.config import settings
from core.models import db_helper, User
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial, UserSchema, UserUpdateAdmin, \
    UserUpdatePartialAdmin
from crud import users as users_crud
from crud.users import update_user
from utils.create_token import ACCESS_TOKEN_TYPE
from utils.dependencies import user_by_id
from utils.check import check_admin
from utils.validate_token import validate_token_type, get_current_token_payload

router = APIRouter(tags=["Users"], prefix=settings.api.prefix, dependencies=[Depends(http_bearer)])


@router.get("/user/{user_id}/", response_model=UserRead | dict)
@cache(expire=30)
async def get_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter),],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: int
):
    user = await users_crud.get_user(session=session, user_id=user_id)
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found!",
        )


@router.get("/users", response_model=list[UserRead] | dict)
@cache(expire=30)
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter),],
        payload: Annotated[dict, Depends(get_current_token_payload)],
):
    if check_admin(payload, role="admin"):
        users = await users_crud.get_all_users(session=session)
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"insufficient permissions to perform the operation",
        )


@router.put("/user/{user_id}/update")
async def update_user_put(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: Annotated[User, Depends(user_by_id)],
        user_update: UserUpdateAdmin,
):
    if check_admin(payload, role="admin"):
        return await users_crud.update_user(
            session=session,
            user=user,
            user_update=user_update,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.patch("/user/{user_id}/update")
async def update_user_partial(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: Annotated[User, Depends(user_by_id)],
        user_update: UserUpdatePartialAdmin,
):
    if check_admin(payload, role="admin"):
        return await users_crud.update_user(
            session=session,
            user=user,
            user_update=user_update,
            partial=True,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.delete("/user/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: User = Depends(user_by_id),
) -> None:
    if check_admin(payload, role="admin"):
        await users_crud.delete_user(session=session, user=user)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )
