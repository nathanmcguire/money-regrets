from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.database import get_session
from backend.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])





@router.get("/", response_model=list[User])
def read_users(session: Session = Depends(get_session)):
    statement = select(User).where(User.is_deleted == False)
    users = session.exec(statement).all()
    return users

@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

read_user

@router.patch("/{user_id}/archive")
def archive_user(user_id: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_archived = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User archived"}






@router.delete("/{user_id}")
def soft_delete_user(user_id: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_deleted = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User soft deleted"}

@router.patch("/{user_id}/restore")
def restore_user(user_id: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_archived = False
    user.is_deleted = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User restored"}


@router.patch("/{user_id}/reactivate")
def reactivate_user(user_id: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user or not user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found or not deleted")
    user.is_deleted = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User reactivated"}



@router.delete("/{user_id}/hard")
def delete_user(user_id: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User permanently deleted"}

