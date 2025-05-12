import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Annotated
from uuid import UUID

from money_regrets.database import get_session
from money_regrets.entities.users import User, UserCreate, UserRead, UserUpdate

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=list[UserRead])
async def get_users(
    session: Session = Depends(get_session),
    offset: Annotated[
        int,
        Query(
            title="Offset",
            description="Number of records to skip",
            ge=0,
        ),
    ] = 0,
    limit: Annotated[
        int,
        Query(
            title="Limit",
            description="Maximum number of records to return",
            ge=1,
        ),
    ] = 10,
    page: Annotated[
        int,
        Query(
            title="Page",
            description="Page number for pagination",
            ge=1,
        ),
    ] = 1,
    sort_by: Annotated[
        str,
        Query(
            title="Sort By",
            description="Field to sort the results by",
        ),
    ] = "uuid",
    order: Annotated[
        str,
        Query(
            title="Order",
            description="Sorting order, either 'asc' for ascending or 'desc' for descending",
        ),
    ] = "asc",
    search: Annotated[
        str | None,
        Query(
            title="Search",
            description="Search term to filter users by name",
            min_length=1,
        ),
    ] = None,
):
    """
    Retrieve a paginated, sorted, and optionally filtered list of users.

    Returns:
    - A list of user objects matching the specified criteria.

    Notes:
    - Pagination is applied using the `page` and `limit` parameters.
    - Sorting is applied based on the `sort_by` and `order` parameters.
    - If a `search` term is provided, users are filtered by names containing the term.
    """
    statement = select(User).where(User.is_deleted.is_(False))

    # Apply search filter if provided
    if search:
        statement = statement.where(User.name.contains(search))

    # Apply sorting
    if order.lower() == "desc":
        statement = statement.order_by(getattr(User, sort_by).desc())
    else:
        statement = statement.order_by(getattr(User, sort_by).asc())

    # Apply pagination
    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)

    users = session.exec(statement).all()
    return users


@router.post("/", response_model=UserRead)
def post_user(body: UserCreate, session: Session = Depends(get_session)):
    """
    Attributes:
    - name (str): The full name of the user. Defaults to 'John Doe'.
    - email (str): The email address of the user. Defaults to 'johndoe@example.com'.
    - password (str): The user's password. This can either be in plaintext or in PHC (Password Hashing Competition) format. Defaults to a pre-defined Argon2id hash.
    """
    new_user = User(**body.dict())  # Create a User instance from UserCreate data
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{uuid}", response_model=UserRead)
def get_user(uuid: UUID, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{uuid}", response_model=UserRead)
def put_user(
    uuid: UUID,
    body: UserCreate,
    session: Session = Depends(get_session),
    mode: Annotated[
        str,
        Query(
            title="Mode",
            description="Mode of operation: 'create' to only create if the user does not exist, 'replace' to delete and recreate if the user exists",
            regex="^(create|replace)$",
        ),
    ] = "create",
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
            session.delete(user)  # Delete the old user instance
        user = User(**body.dict())  # Create a new User instance with the new data
        user.uuid = uuid
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.patch("/{uuid}", response_model=UserRead)
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


@router.delete("/{uuid}", response_model=UserRead, responses={
    200: {
        "description": "User successfully soft-deleted. Returns the user data.",
        "model": UserRead,
    },
    204: {
        "description": "User successfully hard-deleted. No content is returned.",
    },
    404: {
        "description": "User not found.",
    },
})
def delete_user(
    uuid: UUID,
    session: Session = Depends(get_session),
    mode: Annotated[
        str,
        Query(
            title="Mode",
            description="Mode of deletion: 'hard' for permanent deletion, 'soft' for marking as deleted",
            regex="^(hard|soft)$",
        ),
    ] = "soft",
):
    """
    Delete a user by UUID.
    """
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if mode == "soft":
        user.is_deleted = True  # Mark the user as deleted
        session.add(user)
        session.commit()
        logger.debug(f"Soft delete applied to user: {user.uuid}, is_deleted: {user.is_deleted}")
        # Convert the user object to a dictionary and ensure UUID fields are serialized as strings
        user_dict = user.dict()
        user_dict["uuid"] = str(user_dict["uuid"])
        return user  # Return the user with a 200 status code

    if mode == "hard":
        session.delete(user)  # Permanently delete the user
        session.commit()
        logger.debug(f"Hard delete applied to user: {user.uuid}")
        return None  # Return a 204 status code with no content
