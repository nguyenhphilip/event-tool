from typing import Optional
from data.user import User
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from data.db_session import get_session


def find_user_by_email(email: str) -> Optional[User]:
    with get_session() as session:
        return session.query(User).filter(User.email == email).first()


def create_user(name: str, email: str, password: str) -> Optional[User]:
    # prevent duplicates
    if find_user_by_email(email):
        return None

    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_text(password)

    with get_session() as session:
        session.add(user)
        return user


def hash_text(text: str) -> str:
    return crypto.encrypt(text, rounds=171204)


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def login_user(email: str, password: str) -> Optional[User]:
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user or not verify_hash(user.hashed_password, password):
            return None
        return user


def find_user_by_id(user_id: int):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "events": user.events
        }