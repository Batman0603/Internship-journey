# Smart Learning Platform Backend

This is the backend for the Smart Learning Platform, a comprehensive, Flask-based application designed to manage users, courses, assignments, and provide analytics. It features a robust role-based access control (RBAC) system, JWT authentication, and AI-powered features for assignment generation.

## ✨ Features

- **User Management**: Signup, Login, and Profile management with JWT-based authentication.
- **Role-Based Access Control (RBAC)**: Differentiates between `student`, `teacher`, and `admin` roles, each with specific permissions.
- **Course Management**: Teachers can create courses, and students can enroll in them.
- **AI-Powered Assignments**:
  - Teachers can upload notes (`.txt` files) to a Retrieval-Augmented Generation (RAG) system.
  - Generate MCQs or descriptive questions based on the uploaded content.
  - AI-assisted grading capabilities.
- **Asynchronous Tasks**: Background report generation for analytics without blocking the main application thread.
- **Admin Dashboard**: Secure endpoints for admins to manage users and view application logs.
- **Secure & Scalable**: Includes middleware for request logging, rate limiting, and API key protection for sensitive routes.

## 🛠️ Setup and Installation

Follow these steps to get the application running locally.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd smart-learning-backend
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project and add the following configuration. Replace the placeholder values with your actual credentials.

```env
# Database Configuration (MySQL)
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_database_name
MYSQL_HOST=localhost

# JWT Secret Key for signing tokens
JWT_SECRET_KEY=a_very_strong_and_secret_key

# API Key for protecting the /analytics endpoints
ANALYTICS_API_KEY=your_secret_analytics_key
```

### 5. Initialize the Database

Run the custom Flask CLI command to create the database tables and seed initial user data from `mock_data/users.json`.

```bash
flask init-db
```

### 6. Run the Application

Start the Flask development server.

```bash
flask run
```

The application will be running at `http://127.0.0.1:5000`.

## 🚀 API Endpoints

Here is a list of the available API endpoints. Use a client like Bruno or Postman to test them.

| Method | Endpoint                                      | Role(s)             | Description                                                              |
|--------|-----------------------------------------------|---------------------|--------------------------------------------------------------------------|
| **Auth** |
| `POST` | `/auth/signup`                                | Public              | Register a new user.                                                     |
| `POST` | `/auth/login`                                 | Public              | Log in to get a JWT token.                                               |
| **User** |
| `GET` | `/user/profile`                               | Any (Logged In)     | Get the profile of the currently logged-in user.                         |
| `PUT` | `/user/profile`                               | Any (Logged In)     | Update the profile of the currently logged-in user.                      |
| **Admin** |
| `GET` | `/admin/users`                                | Admin               | Get a list of all users.                                                 |
| `GET` | `/admin/users/<id>`                           | Admin               | Get details for a specific user.                                         |
| `PUT` | `/admin/users/<id>/role`                      | Admin               | Update a user's role.                                                    |
| `GET` | `/admin/logs`                                 | Admin               | View the last 100 lines of the application log file.                     |
| **Courses** |
| `POST` | `/api/courses/courses`                        | Teacher             | Create a new course.                                                     |
| `GET` | `/api/courses/courses`                        | Admin, Teacher      | Get a paginated list of all courses.                                     |
| `POST` | `/api/courses/<id>/enroll`                    | Student             | Enroll in a course.                                                      |
| `GET` | `/api/courses/<id>/enrollments`               | Admin, Teacher      | View all students enrolled in a course.                                  |
| **Assignments (AI & RAG)** |
| `POST` | `/api/assignments/upload-notes`               | Teacher             | Upload a `.txt` file to the RAG knowledge base.                          |
| `POST` | `/api/assignments/generate`                   | Teacher             | Generate assignment questions from the knowledge base.                   |
| **Assignments (Management)** |
| `POST` | `/api/assignments/courses/<id>/assignments`   | Teacher             | Create an assignment for a course.                                       |
| `GET` | `/api/assignments/courses/<id>/assignments`   | Teacher, Student    | Get all assignments for a course.                                        |
| `POST` | `/api/assignments/assignments/<id>/submit`    | Student             | Submit an assignment (text or file).                                     |
| `GET` | `/api/assignments/assignments/<id>/submissions` | Teacher             | Get all submissions for an assignment.                                   |
| `PUT` | `/api/assignments/submissions/<id>/grade`     | Teacher             | Grade a student's submission.                                            |
| **Analytics** |
| `GET` | `/analytics/generateReport?apiKey=<key>`      | Public (Key-Protected) | Start a background job to generate a report.                             |
| `GET` | `/analytics/getReport?apiKey=<key>`           | Public (Key-Protected) | Retrieve the generated report.                                           |
| **Misc** |
| `GET` | `/recommendations`                            | Student             | Get course recommendations. (Rate-limited)                               |