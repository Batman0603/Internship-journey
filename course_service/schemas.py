from pydantic import BaseModel
from typing import List, Optional

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    teacher_id: int

    class Config:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True
