from user_service.models import User
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
import bcrypt
from utils.database import SessionLocal # Keep for methods called outside request context

class UserService:
    # Service methods should consistently accept a db session.
    # For methods called outside a request context (like signup), a new session can be created.
    @staticmethod
    def create_user(db: Session, username, email, password, role="student"):
        try:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User(username=username, email=email, password=hashed_pw, role=role)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(db: Session, page: int = 1, limit: int = 10, search: str = None, role: str = None):
        query = db.query(User)

        if role:
            query = query.filter(User.role == role)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )

        total = query.count()
        
        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()
        
        return users, total

    @staticmethod
    def update_user(db: Session, user_id: int, username: str = None, email: str = None):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        if username:
            user.username = username
        if email:
            user.email = email
        
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            # Let the caller (the route) handle the exception
            raise IntegrityError("Username or email already exists", params=None, orig=None)
        
        return user

    @staticmethod
    def update_user_role(db: Session, user_id: int, new_role: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.role = new_role
            db.commit()
            db.refresh(user) # Refresh the object to load the new state
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def get_user_count(db: Session):
        # The session is managed by the caller (request context), so we should not close it here.
        return db.query(User).count()
