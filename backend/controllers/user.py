from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.database import get_session
from backend.models.user import User, UserCreate, UserRead, UserUpdate, UserDelete
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/users", tags=["Users"])



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
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/{uuid}", response_model=UserRead)
def read_user(uuid: str, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{uuid}", response_model=UserRead)
def replace_user(uuid: str, new_user: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_user.id = uuid  # Ensure the ID remains the same
    session.delete(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.patch("/{uuid}", response_model=User)
def update_user(uuid: str, updated_user: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{uuid}")
def soft_delete_user(uuid: str, session: Session = Depends(get_session)):
    user = session.get(User, uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_deleted = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User soft deleted"}