from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from utils.database import Base # Import the shared Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum('student','teacher','admin'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships to link User with Courses and Enrollments
    courses = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    
    # Relationships for assignments
    submissions = relationship("Submission", back_populates="student")
