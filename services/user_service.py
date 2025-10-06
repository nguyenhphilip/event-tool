from typing import Optional
from data.user import User
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import data.db_session as db_session


def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.email == email).first()


def create_user(name: str, email: str, password: str) -> Optional[User]:
    if find_user_by_email(email):
        # account for users who already have emails - so they can't register again
        return None
    
    user = User()
    user.email = email
    user.name = name # pyright: ignore[reportAttributeAccessIssue]
    user.hashed_password = hash_text(password)

    session = db_session.create_session()
    session.add(user)
    session.commit()
    return user


def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def login_user(email:str, password:str) -> Optional[User]:
    session = db_session.create_session()

    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    if not verify_hash(user.hashed_password, password):
        return None
    
    return user


def find_user_by_id(user_id: int):

    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    
    if not user:
        return None
    
    return {"id": user.id, "name": user.name, "email": user.email, "events": user.events}