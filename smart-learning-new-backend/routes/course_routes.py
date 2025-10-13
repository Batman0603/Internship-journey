from flask import Blueprint, request, jsonify, g
from utils.database import get_db
from sqlalchemy.orm import Session
from course_service import service, schemas
from utils.hateoas import add_hateoas_links
from auth.rbac import role_required

course_bp = Blueprint("courses", __name__)

# Teacher creates a new course
@course_bp.route("/new/courses", methods=["POST"])
@role_required(["teacher"])
def create_course():
    """
    Create a new course.
    This endpoint is for teachers to create a new course.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
          properties:
            title:
              type: string
              example: "Introduction to Python"
            description:
              type: string
              example: "A beginner-friendly course on Python programming."
    responses:
      200:
        description: Course created successfully.
      401:
        description: Unauthorized.
    """
    data = request.json
    db: Session = next(get_db())
    course_data = schemas.CourseCreate(**data)
    course = service.CourseService.create_course(db, course_data, teacher_id=g.user.id)
    return jsonify({"message": "Course created", "course_id": course.id, "title": course.title})

# Student enrolls in a course
@course_bp.route("/<int:course_id>/enroll", methods=["POST"]) # This route is fine
@role_required(["student"])
def enroll(course_id):
    """
    Enroll the current student in a course.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - in: path
        name: course_id
        required: true
        type: integer
        description: The ID of the course to enroll in.
    responses:
      200:
        description: Successfully enrolled in the course.
      403:
        description: Access denied. Only students can enroll.
      404:
        description: Course not found.
    """
    db: Session = next(get_db())
    enrollment = service.CourseService.enroll_student(db, course_id, student_id=g.user.id)
    return jsonify({"message": "Enrolled successfully", "course_id": enrollment.course_id})

# Admin/Teacher: View all courses
@course_bp.route("/all", methods=["GET"])
@role_required(["admin", "teacher","student"])
def get_courses():
    """
    Get a list of all courses with pagination, filtering, and sorting.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        schema:
          type: integer
          default: 1
        description: The page number for pagination.
      - in: query
        name: limit
        schema:
          type: integer
          default: 5
        description: The number of items per page.
      - in: query
        name: category
        schema:
          type: string
        description: Filter courses by category (searches in title).
      - in: query
        name: sort
        schema:
          type: string
          enum: [title_asc]
        description: Sort courses by title.
    responses:
      200:
        description: A paginated list of courses.
        schema:
          type: object
          properties:
            total_courses:
              type: integer
            page:
              type: integer
            limit:
              type: integer
            total_pages:
              type: integer
            data:
              type: array
              items:
                type: object
    """
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    category = request.args.get('category', None, type=str)
    sort = request.args.get('sort', 'title_asc', type=str)

    db: Session = next(get_db())
    courses, total_courses = service.CourseService.get_all_courses(db, page, limit, category, sort)

    courses_list = []
    for c in courses:
        course_dict = {
            "id": c.id, 
            "title": c.title, 
            "description": c.description, 
            "teacher_id": c.teacher_id
        }
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
@course_bp.route("/<int:course_id>/enrollments", methods=["GET"])
@role_required(["admin", "teacher"])
def get_course_enrollments(course_id):
    """
    Get all student enrollments for a specific course.
    ---
    tags:
      - Courses
    security:
      - Bearer: []
    parameters:
      - in: path
        name: course_id
        required: true
        type: integer
        description: The ID of the course.
    responses:
      200:
        description: A list of students enrolled in the course.
      403:
        description: Access denied. Only teachers and admins can view enrollments.
      404:
        description: Course not found.
    """
    db: Session = next(get_db())
    course_data = service.CourseService.get_course_enrollments(db, course_id)
    if not course_data:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({
        "course": course_data["course"].title,
        "students": [{"id": s.id, "username": s.username, "role": s.role} for s in course_data["students"]]
    })
