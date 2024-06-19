from typing import Annotated

from fastapi import APIRouter,Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.post import PostRead
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial
from crud import users as users_crud
from crud.users import update_user
from utils.dependencies import user_by_id

router = APIRouter(tags=["Users"], prefix=settings.api.prefix,)


@router.get("/users", response_model=list[UserRead])
async def get_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    users = await users_crud.get_all_users(session=session)
    return users


@router.get("/posts", response_model=list[PostRead])
async def get_posts(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    users = await users_crud.get_all_post(session=session)
    return users


@router.get("/user/{user_id}/", response_model=UserRead)
async def get_user(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        user_id: int
):
    user = await users_crud.get_user(session=session, user_id=user_id)

    return user


@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_create: UserCreate,
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    return user


@router.post("/cr_post", response_model=PostRead)
async def create_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    post_create: PostRead,
):
    post = await users_crud.create_post(
        session=session,
        user_create=post_create,
    )
    return post



@router.put("/user/{user_id}/update")
async def update_user_put(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(user_by_id)],
    user_update: UserUpdate,
):
    return await users_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.patch("/user/{user_id}/update")
async def update_user_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(user_by_id)],
    user_update: UserUpdatePartial,
):
    return await users_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )


@router.delete("/user/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await users_crud.delete_user(session=session, user=user)
