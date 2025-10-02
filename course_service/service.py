from sqlalchemy.orm import Session
from . import models, schemas
from user_service.models import User

class CourseService:
    @staticmethod
    def create_course(db: Session, course: schemas.CourseCreate, teacher_id: int):
        db_course = models.Course(
            title=course.title,
            description=course.description,
            teacher_id=teacher_id
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course

    @staticmethod
    def get_all_courses(db: Session):
        return db.query(models.Course).all()

    @staticmethod
    def enroll_student(db: Session, course_id: int, student_id: int):
        enrollment = models.Enrollment(student_id=student_id, course_id=course_id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def get_course_enrollments(db: Session, course_id: int):
        course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not course:
            return None
        return {
            "course": course,
            "students": [enr.student for enr in course.enrollments]
        }
