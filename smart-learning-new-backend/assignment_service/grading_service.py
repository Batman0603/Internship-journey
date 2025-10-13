from sqlalchemy.orm import Session
from assignment_service.models import Submission

def grade_submission(db: Session, submission_id: int, grade: str):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        return None
    submission.grade = grade
    db.commit()
    db.refresh(submission)
    return submission
