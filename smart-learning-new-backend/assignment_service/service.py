from sqlalchemy.orm import Session
from assignment_service import models, schemas

def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignments(db: Session, course_id: int):
    return db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()

def get_assignment_by_id(db: Session, assignment_id: int):
    return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()

def submit_assignment(db: Session, submission: schemas.SubmissionCreate):
    db_submission = models.Submission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_submissions(db: Session, assignment_id: int):
    return db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()
