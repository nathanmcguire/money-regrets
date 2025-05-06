from sqlmodel import SQLModel, Field
from uuid import UUID
from ulid import ULID
from typing import Optional
from passlib.context import CryptContext

# Initialize Passlib context for hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class User(SQLModel, table=True):
    uuid: UUID = Field(default_factory=lambda: ULID().to_uuid(), primary_key=True)  # Use ULID as the primary key
    name: str
    email: str
    password: str
    is_archived: bool = Field(default=False)
    is_deleted: bool = Field(default=False)

    @classmethod
    def set_password(self, plaintext_password: str):
        """Hashes the plaintext password and sets it to the password field."""
        self.password = pwd_context.hash(plaintext_password)

    @classmethod
    def verify_password(self, plaintext_password: str) -> bool:
        return pwd_context.verify(plaintext_password, self.password)

    @classmethod
    def create(cls, session, name: str, email: str, password: str):
        user = cls(name=name, email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @classmethod
    def read(cls, session, user_id: UUID):
        return session.get(cls, user_id)

    @classmethod
    def update(cls, session, user_id: UUID, name: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
        user = session.get(cls, user_id)
        if user:
            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            if password is not None:
                user.hashed_password = password
            session.commit()
            session.refresh(user)
        return user

    @classmethod
    def delete(cls, session, user_id: UUID):
        user = session.get(cls, user_id)
        if user:
            session.delete(user)
            session.commit()
        return user

    @classmethod
    def soft_delete(cls, session, user_id: UUID):
        """Marks the user as deleted without removing it from the database."""
        user = session.get(cls, user_id)
        if user:
            user.is_deleted = True
            session.commit()
            session.refresh(user)
        return user


class UserCreate(SQLModel):
    name: str
    email: str
    password: str


class UserRead(SQLModel):
    uuid: UUID
    name: str
    email: str
    is_archived: bool
    is_deleted: bool


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_archived: bool
    is_deleted: bool


class UserDelete(SQLModel):
    uuid: UUID
