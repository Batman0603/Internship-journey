from flask import Blueprint, request, jsonify
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

@assignment_bp.route("/assignments/upload-notes", methods=["POST"])
@role_required(["teacher"])
def upload_notes_for_rag(user):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        result = get_rag_service().process_teacher_notes(file_path)
        return jsonify(result), 200

@assignment_bp.route("/assignments/generate", methods=["POST"])
@role_required(["teacher"])
def generate_assignment_questions(user):
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
def create_assignment(user, course_id):
    data = request.json
    db: Session = next(get_db())
    assignment_data = assignment_schemas.AssignmentCreate(
        **data, course_id=course_id, teacher_id=user.id
    )
    assignment = assignment_service.create_assignment(db, assignment_data)
    return jsonify({"message": "Assignment created", "assignment_id": assignment.id}), 201

@assignment_bp.route("/courses/<int:course_id>/assignments", methods=["GET"])
@role_required(["teacher", "student"])
def get_assignments_for_course(user, course_id):
    db: Session = next(get_db())
    assignments = assignment_service.get_assignments(db, course_id)
    return jsonify([{"id": a.id, "title": a.title, "deadline": a.deadline} for a in assignments])

# --- Submission Management Endpoints (Student/Teacher) ---

@assignment_bp.route("/assignments/<int:assignment_id>/submit", methods=["POST"])
@role_required(["student"])
def submit_assignment(user, assignment_id):
    # This endpoint now handles multipart/form-data to allow file uploads
    db: Session = next(get_db())
    
    content = request.form.get('content')
    file_path = None

    # Handle file upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(f"{user.id}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

    if not content and not file_path:
        logging.error(f"Assignment submission failed for assignment {assignment_id} by user {user.id}: No content or file provided.")
        return jsonify({"error": "Submission content or file is required"}), 400

    submission_data = assignment_schemas.SubmissionCreate(
        assignment_id=assignment_id,
        student_id=user.id,
        content=content,
        file_path=file_path
    )
    submission = assignment_service.submit_assignment(db, submission_data)
    return jsonify({"message": "Submission successful", "submission_id": submission.id}), 201

@assignment_bp.route("/assignments/<int:assignment_id>/submissions", methods=["GET"])
@role_required(["teacher"])
def get_submissions_for_assignment(user, assignment_id):
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
def grade_submission(user, submission_id):
    data = request.json
    grade = data.get("grade")
    if not grade:
        return jsonify({"error": "Grade is required"}), 400

    db: Session = next(get_db())
    submission = get_grading_service().grade_submission(db, submission_id, grade)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    
    return jsonify({"message": "Submission graded", "submission_id": submission.id, "grade": submission.grade})