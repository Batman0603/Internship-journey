from flask import Blueprint, request, jsonify
from utils.database import get_db
from sqlalchemy.orm import Session
from course_service import service, schemas
from utils.hateoas import add_hateoas_links
from auth.rbac import role_required

course_bp = Blueprint("courses", __name__)

# Teacher creates a new course
@course_bp.route("/courses", methods=["POST"])
@role_required(["teacher"])
def create_course(user):
    data = request.json
    db: Session = next(get_db())
    course_data = schemas.CourseCreate(**data)
    course = service.CourseService.create_course(db, course_data, teacher_id=user.id)
    return jsonify({"message": "Course created", "course": course.title})

# Student enrolls in a course
@course_bp.route("/courses/<int:course_id>/enroll", methods=["POST"])
@role_required(["student"])
def enroll(user, course_id):
    db: Session = next(get_db())
    enrollment = service.CourseService.enroll_student(db, course_id, student_id=user.id)
    return jsonify({"message": "Enrolled successfully", "course_id": enrollment.course_id})

# Admin/Teacher: View all courses
@course_bp.route("/courses", methods=["GET"])
@role_required(["admin", "teacher"])
def get_courses(user):
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    category = request.args.get('category', None, type=str)
    sort = request.args.get('sort', None, type=str)

    db: Session = next(get_db())
    courses, total_courses = service.CourseService.get_all_courses(db, page, limit, category, sort)

    courses_list = []
    for c in courses:
        course_dict = {"id": c.id, "title": c.title, "teacher_id": c.teacher_id}
        # Add HATEOAS links for each course
        courses_list.append(add_hateoas_links("courses", course_dict))

    return jsonify({
        "total_courses": total_courses,
        "page": page,
        "limit": limit,
        "total_pages": (total_courses + limit - 1) // limit,
        "data": courses_list
    })


# Admin/Teacher: View course enrollments
@course_bp.route("/courses/<int:course_id>/enrollments", methods=["GET"])
@role_required(["admin", "teacher"])
def get_course_enrollments(user, course_id):
    db: Session = next(get_db())
    course_data = service.CourseService.get_course_enrollments(db, course_id)
    if not course_data:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({
        "course": course_data["course"].title,
        "students": [{"id": s.id, "username": s.username, "role": s.role} for s in course_data["students"]]
    })
