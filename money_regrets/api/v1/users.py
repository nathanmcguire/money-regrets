from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from money_regrets.database import get_session
from money_regrets.entities.users import User, UserCreate, UserRead, UserUpdate
from typing import Annotated
from fastapi import Query
from uuid import UUID

router = APIRouter()

# Core CRUD operations for User model

@router.get("/", response_model=list[UserRead])
async def read_users(
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
    statement = select(User).where(User.is_deleted == False)

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
def create_user(body: UserCreate, session: Session = Depends(get_session)):
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
def read_user(uuid: UUID, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{uuid}", response_model=UserRead)
def replace_user(uuid: UUID, body: UserCreate, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)  # Delete the old user instance
    user = User(**body.dict())  # Create a new User instance with the new data
    user.uuid = uuid
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.patch("/{uuid}", response_model=UserRead)
def update_user(uuid: UUID, body: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in body.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{uuid}", status_code=204)
def delete_user(uuid: UUID, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return