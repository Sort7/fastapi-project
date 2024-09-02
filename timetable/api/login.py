from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.token import TokenInfo
from authentication.utils import validate_password, http_bearer
from core.config import settings
from core.models import db_helper, User
from core.schemas.user import UserCreate, UserBase, UserUpdate, UserUpdatePartial
from crud import users as users_crud
from crud.users import get_user_by_username
from utils.create_token import create_access_token, create_refresh_token, REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE
from utils.dependencies import user_by_id, user_by_payload
from utils.validate_token import get_current_token_payload, validate_token_type

router = APIRouter(tags=["Auth"], prefix=settings.api.prefix, dependencies=[Depends(http_bearer)])


@router.post("/create", response_model=UserBase)
async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: UserCreate,
):
    user = await users_crud.create_user(
        session=session,
        user_data=user_data,
    )
    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        username: str = Form(),
        password: str = Form(),
):
    user = await get_user_by_username(
        session=session,
        username=username,
    )

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if user == None:
        raise unauthed_exc

    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc

    if not user.is_active == True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True, )
async def auth_refresh_jwt(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
):
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    user = await users_crud.get_user(session=session, user_id=payload.get("sub"))
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/users/me/")
async def auth_user_check_self_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
):
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    user = await users_crud.get_user(session=session, user_id=payload.get("sub"))
    return {
        "username": user.username,
        "email": user.email,
    }


@router.put("/user/me_update")
async def update_me_put(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user: Annotated[User, Depends(user_by_payload)],
        user_update: UserUpdate,
):
    try:
        return await users_crud.update_user(
            session=session,
            user=user,
            user_update=user_update,
        )
    except Exception:
        return {"status": "error", "details": "Error updating the user by the method - put"}


@router.patch("/me_update")
async def update_user_partial(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user: Annotated[User, Depends(user_by_payload)],
        user_update: UserUpdatePartial,
):
    try:
        return await users_crud.update_user(
            session=session,
            user=user,
            user_update=user_update,
            partial=True,
        )
    except Exception:
        return {"status": "error", "details": "Error updating the user by the method - patch"}
