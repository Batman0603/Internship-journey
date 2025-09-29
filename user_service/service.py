from user_service.models import User, Base
from utils.database import engine, SessionLocal
from sqlalchemy.exc import IntegrityError
import bcrypt

# Create tables
Base.metadata.create_all(bind=engine)

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
    def get_user_by_email(email):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
        finally:
            db.close()
