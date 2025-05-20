import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from typing import Annotated
from .models import User, UserCreate, UserRead, UserUpdate, UsersRead
from money_regrets_api.database import get_session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

users_router = APIRouter(tags=["Users"])

@users_router.get("/", response_model=list[UsersRead])
async def get_users(
    session: Session = Depends(get_session),
    offset: Annotated[int, Query(title="Offset", description="Number of records to skip", ge=0)] = 0,
    limit: Annotated[int, Query(title="Limit", description="Maximum number of records to return", ge=1)] = 10,
    page: Annotated[int, Query(title="Page", description="Page number for pagination", ge=1)] = 1,
    sort_by: Annotated[str, Query(title="Sort By", description="Field to sort the results by")] = "uuid",
    order: Annotated[str, Query(title="Order", description="Sorting order, either 'asc' for ascending or 'desc' for descending")] = "asc",
    search: Annotated[str | None, Query(title="Search", description="Search term to filter users by name", min_length=1)] = None,
):
    statement = select(User).where(User.is_deleted.is_(False))
    if search:
        statement = statement.where(User.name.contains(search))
    if order.lower() == "desc":
        statement = statement.order_by(getattr(User, sort_by).desc())
    else:
        statement = statement.order_by(getattr(User, sort_by).asc())
    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)
    users = session.exec(statement).all()
    return users

@users_router.post("/", response_model=UserRead)
def post_user(body: UserCreate, session: Session = Depends(get_session)):
    new_user = User(**body.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@users_router.get("/{uuid}", response_model=UserRead)
def get_user(uuid: UUID, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.put("/{uuid}", response_model=UserRead)
def put_user(
    uuid: UUID,
    body: UserCreate,
    session: Session = Depends(get_session),
    mode: Annotated[str, Query(title="Mode", description="Mode of operation: 'create' to only create if the user does not exist, 'replace' to delete and recreate if the user exists", regex="^(create|replace)$")] = "create",
):
    user = session.get(User, uuid)
    if mode == "create":
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        user = User(**body.dict())
        user.uuid = uuid
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    if mode == "replace":
        if user:
            session.delete(user)
        user = User(**body.dict())
        user.uuid = uuid
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@users_router.patch("/{uuid}", response_model=UserRead)
def patch_user(uuid: UUID, body: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in body.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@users_router.delete("/{uuid}", response_model=UserRead, responses={
    200: {"description": "User successfully soft-deleted. Returns the user data.", "model": UserRead},
    204: {"description": "User successfully hard-deleted. No content is returned."},
    404: {"description": "User not found."},
})
def delete_user(
    uuid: UUID,
    session: Session = Depends(get_session),
    mode: Annotated[str, Query(title="Mode", description="Mode of deletion: 'hard' for permanent deletion, 'soft' for marking as deleted", regex="^(hard|soft)$")] = "soft",
):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if mode == "soft":
        user.is_deleted = True
        session.add(user)
        session.commit()
        logger.debug(f"Soft delete applied to user: {user.uuid}, is_deleted: {user.is_deleted}")
        user_dict = user.dict()
        user_dict["uuid"] = str(user_dict["uuid"])
        return user
    if mode == "hard":
        session.delete(user)
        session.commit()
        logger.debug(f"Hard delete applied to user: {user.uuid}")
        return None
