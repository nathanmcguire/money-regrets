from sqlmodel import SQLModel, Field
from uuid import UUID
from ulid import ULID
from typing import Optional
from passlib.context import CryptContext

# Initialize Passlib context for hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class User(SQLModel, table=True):
    """
    Represents a User entity for the database, with fields and methods for managing user data.
    Attributes:
        uuid (UUID): The primary key for the user, generated using ULID.
        name (str): The name of the user. Defaults to "John Doe".
        email (str): The email address of the user. Defaults to "johndoe@example.com".
        password (str): The hashed password of the user. Defaults to a pre-hashed value.
        is_archived (bool): Indicates if the user is archived. Defaults to False.
        is_deleted (bool): Indicates if the user is deleted. Defaults to False.
    """
    __tablename__ = "Users"  # Set the table name to "Users"
    
    uuid: UUID = Field(default_factory=lambda: ULID().to_uuid(), primary_key=True)  # Use ULID as the primary key
    name: str = Field(default="John Doe")
    email: str = Field(default="johndoe@example.com")
    password: str = Field(default="$argon2id$v=19$m=65536,t=3,p=4$WzG6p+Y9A1aTkgWj1xKziQ$FhCbCMRK3S6kND7rOUPKD2P1VzV0jEjv0TP9k8rMg0I")
    is_archived: bool = Field(default=False)
    is_deleted: bool = Field(default=False)


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
    def set_password(self, password: str):
        """
        Detects if the password is plaintext or already hashed.
        If it is plaintext, hashes it and sets it to the password field.
        If it is already hashed, stores the hash directly.
        """
        if password.startswith("$argon2id$"):
            # Assume the password is already hashed
            self.password = password
        else:
            # Hash the plaintext password
            self.password = pwd_context.hash(password)


    @classmethod
    def verify_password(self, plaintext_password: str) -> bool:
        return pwd_context.verify(plaintext_password, self.password)


class UserCreate(SQLModel):
    """
    Represents a user creation model with default values.
    """
    name: str = Field(default="John Doe")
    email: str = Field(default="johndoe@example.com")
    password: str = Field(default="$argon2id$v=19$m=65536,t=3,p=4$WzG6p+Y9A1aTkgWj1xKziQ$FhCbCMRK3S6kND7rOUPKD2P1VzV0jEjv0TP9k8rMg0I")
    is_archived: Optional[bool] = Field(default=False)
    is_deleted: Optional[bool] = Field(default=False)


class UserRead(SQLModel):
    """
    Represents a user read model for retrieving user data.
    """
    uuid: UUID
    name: str
    email: str
    is_archived: bool
    is_deleted: bool


class UserUpdate(SQLModel):
    """
    UserUpdate is a data model representing the fields that can be updated for a user.
    """
    name: Optional[str] = Field(default="John Doe")
    email: Optional[str] = Field(default="johndoe@example.com")
    password: Optional[str] = Field(default="$argon2id$v=19$m=65536,t=3,p=4$WzG6p+Y9A1aTkgWj1xKziQ$FhCbCMRK3S6kND7rOUPKD2P1VzV0jEjv0TP9k8rMg0I")
    is_archived: Optional[bool] = Field(default=False)
    is_deleted: Optional[bool] = Field(default=False)
