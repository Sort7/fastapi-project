from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial
from crud import users as users_crud
from crud.users import update_user
from utils.dependencies import user_by_id

router = APIRouter(tags=["Users"], prefix=settings.api.prefix,)


@router.get("/user/{user_id}/", response_model=UserRead)
async def get_user(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        user_id: int
): #  -> UserRead | dict
    try:
        user = await users_crud.get_user(session=session, user_id=user_id)
        if user is not None:
            return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found!",
        )
        return user
    except Exception:
        return {"status": "error", "details": "Error when outputting user data"}

@router.get("/users", response_model=list[UserRead] | dict)
async def get_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> list[UserRead] | dict:
    try:
        users = await users_crud.get_all_users(session=session)
        return users
    except Exception:
        return {"status": "error", "details": "Аn error occurred when forming a list of users"}



@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_create: UserCreate,
):
    try:
        user = await users_crud.create_user(
            session=session,
            user_create=user_create,
        )
        return user
    except Exception:
        return {"status": "error", "details": "Error when creating a user"}


@router.put("/user/{user_id}/update")
async def update_user_put(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(user_by_id)],
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


@router.patch("/user/{user_id}/update")
async def update_user_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(user_by_id)],
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


@router.delete("/user/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    try:
        await users_crud.delete_user(session=session, user=user)
    except Exception:
        return {"status": "error", "details": "User deletion error"}
