# Habit Tracker API

A simple Habit Tracker built with FastAPI and SQLModel that helps users create habits, track daily completion, and monitor their progress through streak calculations.

This project was built as part of my backend development learning journey to gain hands-on experience with REST APIs, database integration, authentication, and clean project structure.

---

## Features

### Habit Management
- Create new habits
- View all habits
- Edit existing habits
- Delete habits
- Mark habits as completed

### Streak Tracking
- Calculate current streak
- Calculate maximum streak
- Prevent duplicate completions for the same day

### Authentication
- User registration (signup)
- User login
- Password hashing using Passlib
- JWT-based authentication
- Protected API routes

### Database
- SQLite database
- SQLModel ORM
- Automatic table creation

---

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
- Passlib
- JWT Authentication
- Pydantic

---

## Project Structure

```text
Habit_Tracker/
│
├── app/
│   ├── auth.py
│   ├── db.py
│   ├── models.py
│   ├── routes.py
│   ├── security.py
│   ├── service.py
│   └── validator.py
│
├── Habitdb.db
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd Habit_Tracker
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn app.routes:app --reload
```

Server starts at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Authentication Flow

### Signup

```http
POST /signup
```

Example Request:

```json
{
  "username": "deepak",
  "email": "deepak@example.com",
  "password": "mypassword"
}
```

---

### Login

```http
POST /login
```

Example Request:

```json
{
  "email": "deepak@example.com",
  "password": "mypassword"
}
```

Example Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

---

### Authorize Requests

1. Login and copy the token.
2. Click the **Authorize** button in Swagger UI.
3. Enter:

```text
Bearer <your_token>
```

4. Access protected endpoints.

---

## Habit Endpoints

### Create Habit

```http
POST /habits
```

### Get All Habits

```http
GET /habits
```

### Edit Habit

```http
PATCH /habits/{habit_id}
```

### Delete Habit

```http
DELETE /habits/{habit_id}
```

### Mark Habit Completed

```http
PATCH /habits/{habit_id}/complete
```

### Current Streak

```http
GET /habits/{habit_id}/streak
```

### Maximum Streak

```http
GET /habits/{habit_id}/max-streak
```

---

## Validation Rules

### Habit Name
- Cannot be empty
- Maximum 50 characters
- Letters, numbers, and spaces only
- Must contain at least one letter

### Category
Allowed values:

- Health
- Productivity
- Personal
- Social
- Other

### User Registration
- Username must be unique
- Email must be unique
- Passwords are stored as hashes, not plain text

---

## What I Learned

While building this project, I practiced:

- REST API design
- FastAPI routing
- Dependency Injection
- SQLModel database operations
- Password hashing
- JWT authentication
- Error handling
- Input validation
- Project organization

---

## Future Improvements

Planned improvements include:

- Habit ownership (multi-user habits)
- Reminder notifications
- Habit statistics dashboard
- Pagination
- Refresh tokens
- Docker support
- Deployment to cloud platforms

---

## Author

Deepak

Backend development and machine learning enthusiast currently focused on building practical projects and strengthening software engineering fundamentals.