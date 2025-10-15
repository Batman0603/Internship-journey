from flask import Blueprint, request, jsonify, g
from werkzeug.utils import secure_filename
import logging
import os
from utils.database import get_db
from sqlalchemy.orm import Session
from auth.rbac import role_required
from assignment_service import service as assignment_service, schemas as assignment_schemas

# --- Lazy Loading for RAG and Grading Services ---
# These services can be slow to initialize (e.g., downloading models).
# We defer their import and initialization until they are first needed.

def get_rag_service():
    from assignment_service import rag_service
    return rag_service

def get_grading_service():
    from assignment_service import grading_service
    return grading_service

# --- End Lazy Loading ---

assignment_bp = Blueprint("assignments", __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- RAG & Content Generation Endpoints (Teacher) ---

@assignment_bp.route("/upload-notes", methods=["POST"])
@role_required(["teacher"])
def upload_notes_for_rag():
    """
    Upload a .txt file of notes for the RAG system.
    ---
    tags:
      - Assignments (RAG)
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: The .txt file to upload.
    responses:
      200:
        description: File processed successfully.
      400:
        description: No file part or no selected file.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        # Prefix with user ID to avoid filename conflicts
        filename = secure_filename(f"{g.user.id}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        result = get_rag_service().process_teacher_notes(file_path)
        return jsonify(result), 200

@assignment_bp.route("/generate", methods=["POST"])
@role_required(["teacher"])
def generate_assignment_questions():
    """
    Generate assignment questions using the RAG system.
    ---
    tags:
      - Assignments (RAG)
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              example: "What are the key concepts of blockchain?"
            mode:
              type: string
              enum: [mcq, descriptive]
              default: mcq
            num_q:
              type: integer
              default: 5
    responses:
      200:
        description: Generated questions.
      400:
        description: Query is required.
    """
    data = request.json
    query = data.get("query")
    mode = data.get("mode", "mcq") # 'mcq' or 'descriptive'
    num_q = data.get("num_q", 5)

    if not query:
        return jsonify({"error": "Query is required"}), 400
        
    questions = get_rag_service().create_assignment_with_rag(query, mode, num_q)
    return jsonify(questions), 200

# --- Assignment Management Endpoints (Teacher/Student) ---

@assignment_bp.route("/courses/<int:course_id>/assignments", methods=["POST"])
@role_required(["teacher"])
def create_assignment(course_id):
    """
    Create a new assignment for a course.
    ---
    tags:
      - Assignments (Management)
    security:
      - Bearer: []
    parameters:
      - in: path
        name: course_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [title, description, type, deadline]
          properties:
            title:
              type: string
            description:
              type: string
            type:
              type: string
              enum: [mcq, descriptive]
            deadline:
              type: string
              format: date-time
    responses:
      201:
        description: Assignment created successfully.
    """
    data = request.json
    db: Session = next(get_db())
    assignment_data = assignment_schemas.AssignmentCreate(
        **data, course_id=course_id, teacher_id=g.user.id
    )
    assignment = assignment_service.create_assignment(db, assignment_data)
    return jsonify({"message": "Assignment created", "assignment_id": assignment.id}), 201

@assignment_bp.route("/courses/<int:course_id>/assignments", methods=["GET"])
@role_required(["teacher", "student"])
def get_assignments_for_course(course_id):
    """
    Get all assignments for a specific course.
    ---
    tags:
      - Assignments (Management)
    security:
      - Bearer: []
    parameters:
      - in: path
        name: course_id
        required: true
        type: integer
    responses:
      200:
        description: A list of assignments for the course.
      404:
        description: Course not found.
    """
    db: Session = next(get_db())
    assignments = assignment_service.get_assignments(db, course_id)
    return jsonify([{"id": a.id, "title": a.title, "deadline": a.deadline} for a in assignments])

# --- Submission Management Endpoints (Student/Teacher) ---

@assignment_bp.route("/assignments/<int:assignment_id>/submit", methods=["POST"])
@role_required(["student"])
def submit_assignment(assignment_id):
    """
    Submit work for an assignment.
    Can be a text submission, a file upload, or both.
    ---
    tags:
      - Assignments (Submissions)
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: path
        name: assignment_id
        required: true
        type: integer
      - in: formData
        name: content
        type: string
        description: Text content for the submission.
      - in: formData
        name: file
        type: file
        description: A file to upload as the submission.
    responses:
      201:
        description: Submission successful.
      400:
        description: Submission content or file is required.
      404:
        description: Assignment not found.
      500:
        description: Database error during submission.
    """
    # This endpoint now handles multipart/form-data to allow file uploads----descriptive
    db: Session = next(get_db())
    
    # Check if the assignment exists before proceeding
    assignment = assignment_service.get_assignment_by_id(db, assignment_id)
    if not assignment:
        logging.error(f"Submission failed: User {g.user.id} tried to submit to non-existent assignment {assignment_id}.")
        return jsonify({"error": f"Assignment with id {assignment_id} not found."}), 404

    content = request.form.get('content')
    file_path = None

    # Handle file upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(f"{g.user.id}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

    if not content and not file_path:
        logging.error(f"Submission failed for assignment {assignment_id} by user {g.user.id}: No content or file provided.")
        return jsonify({"error": "Submission content or file is required"}), 400

    submission_data = assignment_schemas.SubmissionCreate(
        assignment_id=assignment_id,
        student_id=g.user.id,
        content=content,
        file_path=file_path
    )
    try:
        submission = assignment_service.submit_assignment(db, submission_data)
    except Exception as e:
        # Catch potential IntegrityError or other DB errors
        logging.error(f"Database error on submission for assignment {assignment_id} by user {g.user.id}: {e}")
        return jsonify({"error": "Could not process submission due to a database error."}), 500
    return jsonify({"message": "Submission successful", "submission_id": submission.id}), 201

@assignment_bp.route("/assignments/<int:assignment_id>/submissions", methods=["GET"])
@role_required(["teacher"])
def get_submissions_for_assignment(assignment_id):
    """
    Get all submissions for a specific assignment.
    ---
    tags:
      - Assignments (Submissions)
    security:
      - Bearer: []
    parameters:
      - in: path
        name: assignment_id
        required: true
        type: integer
    responses:
      200:
        description: A list of submissions.
      404:
        description: Assignment not found.
    """
    db: Session = next(get_db())
    submissions = assignment_service.get_submissions(db, assignment_id)
    return jsonify([{
        "id": s.id, 
        "student_id": s.student_id, 
        "submitted_at": s.submitted_at,
        "grade": s.grade
    } for s in submissions])

# --- Grading Endpoint (Teacher) ---

@assignment_bp.route("/submissions/<int:submission_id>/grade", methods=["PUT"])
@role_required(["teacher"])
def grade_submission(submission_id):
    """
    Grade a student's submission.
    ---
    tags:
      - Assignments (Submissions)
    security:
      - Bearer: []
    parameters:
      - in: path
        name: submission_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [grade]
          properties:
            grade:
              type: string
              example: "95"
    responses:
      200:
        description: Submission graded successfully.
      400:
        description: Grade is required.
      404:
        description: Submission not found.
    """
    data = request.json
    grade = data.get("grade")
    if not grade:
        return jsonify({"error": "Grade is required"}), 400

    db: Session = next(get_db())
    submission = get_grading_service().grade_submission(db, submission_id, grade)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    
    return jsonify({"message": "Submission graded", "submission_id": submission.id, "grade": submission.grade})