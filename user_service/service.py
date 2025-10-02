from user_service.models import User, Base
from utils.database import engine, SessionLocal
from sqlalchemy.exc import IntegrityError
import bcrypt

class UserService:

    @staticmethod
    def create_user(username, email, password, role="student"):
        db = SessionLocal()
        try:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User(username=username, email=email, password=hashed_pw, role=role)
            db.add(user)
            db.commit()
            return user
        except IntegrityError:
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def get_user_by_id(user_id):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_user_by_email(email):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_users():
        db = SessionLocal()
        try:
            return db.query(User).all()
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def update_user(user_id, username=None, email=None):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None

            if username:
                user.username = username
            if email:
                user.email = email
            
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            return "IntegrityError" # Indicates a duplicate username/email
        finally:
            db.close()

    @staticmethod
    def update_user_role(user_id, new_role):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.role = new_role
                db.commit()
                db.refresh(user) # Refresh the object to load the new state
            return user
        finally:
            db.close()

    @staticmethod
    def get_user_count():
        db = SessionLocal()
        try:
            return db.query(User).count()
        except Exception as e:
            print(f"[ERROR] {e}")
            return 0 # Return 0 if there's an error, implying no users found
        finally:
            db.close()
