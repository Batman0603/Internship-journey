from flask import Blueprint, jsonify, g
from auth.rbac import login_required, role_required
from course_service.service import CourseService
from sqlalchemy.orm import Session

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/admin/dashboard")
@role_required(["admin"])
def admin_dashboard():
    """
    Admin dashboard endpoint.
    ---
    tags:
      - Dashboard
    security:
      - cookieAuth: []
    responses:
      200:
        description: Welcome message for admin.
      403:
        description: Access denied.
    """
    return jsonify({"message": f"Welcome to the admin dashboard, {g.user.username}!"})

@dashboard_bp.route("/teacher/dashboard")
@role_required(["teacher"])
def teacher_dashboard():
    """
    Teacher dashboard endpoint.
    ---
    tags:
      - Dashboard
    security:
      - cookieAuth: []
    responses:
      200:
        description: Welcome message for teacher.
      403:
        description: Access denied.
    """
    return jsonify({"message": f"Welcome to the teacher dashboard, {g.user.username}!"})

@dashboard_bp.route("/student/dashboard")
@login_required
def student_dashboard():
    """
    Student dashboard endpoint.
    ---
    tags:
      - Dashboard
    security:
      - cookieAuth: []
    responses:
      200:
        description: Welcome message and list of courses for the student.
      403:
        description: Access denied.
    """
    db: Session = g.db
    enrolled_course_ids = {enrollment.course_id for enrollment in g.user.enrollments}
    
    # Fetch all courses, assuming we don't need pagination for the dashboard view for now
    all_courses, _ = CourseService.get_all_courses(db, page=1, limit=100)

    courses_with_status = []
    for course in all_courses:
        courses_with_status.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "is_enrolled": course.id in enrolled_course_ids
        })

    return jsonify({
        "message": f"Welcome to the student dashboard, {g.user.username}!",
        "courses": courses_with_status
    })