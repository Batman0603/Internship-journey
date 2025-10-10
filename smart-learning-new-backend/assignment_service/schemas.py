from pydantic import BaseModel
from typing import Optional
import datetime

class AssignmentCreate(BaseModel):
    course_id: int
    teacher_id: int
    title: str
    description: Optional[str] = None
    type: str
    deadline: datetime.datetime

class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int
    content: Optional[str] = None
    file_path: Optional[str] = None
