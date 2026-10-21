# Hospital Management System API

A secure, modular, and production-ready RESTful API built with FastAPI, SQLAlchemy, Pydantic, and SQLite. Designed following clean code principles, the system manages hospital workflows including user authentication with JWT, doctor profiles, patient records, and an automated testing suite.

---

## Key Features

- **User Authentication & Authorization:**
  - Secure user registration and login endpoints (`/auth/register`, `/auth/login`, `/auth/me`).
  - Password hashing using `passlib` and `bcrypt`.
  - Token-based route protection for state-changing operations (`POST`, `PUT`, `DELETE`).
  - Full compatibility with Swagger UI's Authorize button (`OAuth2PasswordBearer`).

- **Doctor Management:**
  - Full CRUD operations (`/doctors`).
  - Public read endpoints and JWT-protected create, update, and delete endpoints.

- **Patient Records:**
  - Full CRUD operations (`/patients`).
  - Automatic validation of doctor existence (`doctor_id`) upon patient creation and update.
  - Public read endpoints and JWT-protected modification endpoints.

- **Data Validation & Response Schemas:**
  - Powered by Pydantic v2 (`schemas.py`) for request body validation and response serialization (`response_model`).
  - Prevents mass-assignment vulnerabilities and ensures clean API contracts.

- **Automated Testing Suite:**
  - Comprehensive unit and integration tests using Pytest and HTTPX.
  - Isolated test execution with an in-memory SQLite database (`sqlite:///:memory:` with `StaticPool`).

- **Web Interface:**
  - Jinja2 template integration rendering a clean home page at `/`.

---

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Database & ORM:** SQLite, SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Authentication:** Passlib (bcrypt), Python-JOSE (JWT)
- **Testing:** Pytest, HTTPX, SQLAlchemy StaticPool
- **ASGI Server:** Uvicorn
- **Templating:** Jinja2
- **Version Control:** Git & GitHub

---

## Project Structure

```text
Medical_app/
│
├── router/             # Modular API route handlers
│   ├── auth.py         # Authentication & JWT endpoints
│   ├── doctors.py      # Doctor CRUD endpoints (protected)
│   └── patients.py     # Patient CRUD endpoints (protected)
│
├── templates/          # HTML templates for web UI
│   └── index.html      # Landing page
│
├── tests/              # Automated testing suite
│   ├── conftest.py     # Test fixtures & in-memory DB setup (StaticPool)
│   └── test_doctors.py # Router & Auth integration tests
│
├── database.py         # SQLAlchemy engine & session setup
├── main.py             # Application entrypoint & router initialization
├── model.py            # SQLAlchemy ORM models (User, Doctor, Patient)
├── schemas.py          # Pydantic schemas (Request & Response models)
├── pytest.ini          # Pytest configuration file
├── req.txt             # Project dependencies
├── .gitignore          # Excluded files (DB, __pycache__, venv)
└── README.md           # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.11 or Python 3.12
- Git installed

### Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cristianasilviaB/Medical_App.git
   cd Medical_App
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r req.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the Web Dashboard & API Docs:**
   - Web App: http://127.0.0.1:8000
   - Interactive API Documentation (Swagger UI): http://127.0.0.1:8000/docs
   - Alternative API Documentation (ReDoc): http://127.0.0.1:8000/redoc

---

## Running Automated Tests

Run the test suite using `pytest`:

```powershell
python -m pytest
```

The tests execute against a temporary in-memory database (`sqlite:///:memory:`) using `StaticPool` to ensure isolated, fast, and repeatable runs without affecting the local `hospital.db` file.