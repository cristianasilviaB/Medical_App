# Medical Hospital Management System API

An enterprise-grade Python Backend API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, designed following a strict **3-Layer Architecture** (Routers, Services, Repositories) and containerized with **Docker Compose** for scalable hospital administration, patient record management, and clinical analytics.

## Key Technologies

* **Framework:** FastAPI (Python 3.12)

* **Database & ORM:** PostgreSQL 16 (Alpine), SQLAlchemy 2.0 (`psycopg2-binary` / `psycopg`)

* **Containerization & Orchestration:** Docker, Docker Compose

* **Data Validation & DTOs:** Pydantic v2

* **Security & Authentication:** OAuth2 with JWT (`PyJWT`, `Passlib` with `Bcrypt`)

* **Testing & Quality Assurance:** Pytest, Pytest-Cov (93% coverage on PostgreSQL)

* **Logging & Audit:** Custom FastAPI Middleware (`LoggingMiddleware`)

## System Architecture & Layering

The application enforces a strict separation of concerns to maximize maintainability, testability, and enterprise scalability:

![Architecture](images/architecture.png)



### Layer Responsibilities

1. **Router Layer (`router/`)**: Handles HTTP endpoint registration, query/path parameters, JWT token extraction, and response serialisation.

2. **Service Layer (`services/`)**: Encapsulates core business rules (preventing doctor schedule conflicts, duplicate active patient checks, soft-deletion handling, medical status workflows, and revenue calculations).

3. **Repository Layer (`repositories/`)**: Manages raw database interactions via SQLAlchemy (CRUD operations, filtering, pagination, and SQL aggregations).

### Container Infrastructure (Docker Compose)

The production stack runs as an isolated multi-container setup orchestrated via `docker-compose.yml`:

* **`medical_db` (`postgres:16-alpine`):** Dedicated PostgreSQL database service backed by a persistent Docker volume (`postgres_data`) and automated health checks (`pg_isready`).

* **`medical_api` (`web`):** FastAPI application container configured with `depends_on` (`condition: service_healthy`) and `restart: unless-stopped` policies so the API starts only after PostgreSQL is ready to accept connections.

## Relational Schema (ERD)

The database schema manages relationship integrity across core healthcare entities:

![Relational Schema](images/relational_Schema.png)

## Request Lifecycle & Validation Flow

When booking an appointment, request data flows through multi-stage validation checks before persistence:

![Request Lifecycle](images/request_lifecycle.png)

## Core Modules & Business Features

* **Authentication & Authorization:** User registration, password hashing (`bcrypt`), and JWT Bearer Token validation.

* **Doctor Management:** Full CRUD operations for clinical staff and specializations.

* **Patient Management:** Full CRUD with duplicate active record prevention, **Soft Delete** support (`is_deleted=True`) to preserve clinical history, and a dedicated history retrieval endpoint (`GET /patients/{id}/history`).

* **Medical Services Catalog:** Configurable procedures with pricing and duration (in minutes).

* **Appointment Management:**

  * Automated overlap conflict prevention per doctor based on procedure duration:
    `requested_start < existing_end` **and** `requested_end > existing_start`

  * Status lifecycle management (`scheduled`, `completed`, `cancelled`).

  * Automatic time slot release upon appointment cancellation.

  * Search filtering (by doctor, patient, status) and pagination support (`skip`, `limit`).

* **Analytics & Reporting Module:** Aggregate stats for hospital metrics, completed vs. cancelled bookings, revenue by doctor, and revenue by medical service.

* **Audit & Middleware:** Custom HTTP request logging and performance duration header (`X-Process-Time`).

## Project Directory Structure

```
Medical_app/
├── images/                 # Architecture, ERD & Request Lifecycle diagrams
├── repositories/           # Data Access Layer (SQLAlchemy ORM Queries)
│   ├── analytics_repository.py
│   ├── appointment_repository.py
│   ├── doctor_repository.py
│   ├── patient_repository.py
│   └── service_repository.py
├── services/               # Business Logic Layer (Domain Validations)
│   ├── analytics_service.py
│   ├── appointment_service.py
│   ├── doctor_service.py
│   ├── medical_service_service.py
│   └── patient_service.py
├── router/                 # API Controllers Layer (FastAPI Endpoints)
│   ├── analytics.py
│   ├── appointments.py
│   ├── auth.py
│   ├── doctors.py
│   ├── patients.py
│   └── services.py
├── tests/                  # Automated Test Suite (Pytest on PostgreSQL)
│   ├── conftest.py
│   ├── test_analytics.py
│   ├── test_appointments.py
│   ├── test_doctors.py
│   ├── test_patients.py
│   └── test_services.py
├── Dockerfile              # Multi-service API container definition
├── docker-compose.yml      # Multi-container orchestration (FastAPI + PostgreSQL)
├── database.py             # Database Engine & Session Local Setup
├── main.py                 # FastAPI Application Gateway & Router Registration
├── middleware.py           # Logging & Performance Middleware
├── model.py                # Database Relational Entities (SQLAlchemy Models)
├── schemas.py              # Data Transfer Objects (Pydantic Schemas)
├── pytest.ini              # Pytest & Code Coverage configuration
└── req.txt                 # Project Dependencies

```

## Getting Started (Docker & PostgreSQL)

### Prerequisites

* **Docker Desktop** installed and running

* **Git** installed

### 1. Clone the Repository

```
git clone https://github.com/cristianasilviaB/Medical_App.git
cd Medical_App

```

### 2. Build and Start the Containers

Start both the **PostgreSQL 16** database and the **FastAPI** backend in detached mode:

```
docker compose up -d --build

```

* The API server runs at `http://localhost:8000`.

* Interactive Swagger UI documentation is available at `http://localhost:8000/docs`.

* Alternative ReDoc documentation is available at `http://localhost:8000/redoc`.

### 3. Useful Docker Management Commands

* **Check running containers:**

  ```
  docker ps
  
  ```

* **View live API logs:**

  ```
  docker compose logs -f web
  
  ```

* **Stop containers (preserves PostgreSQL data in `postgres_data` volume):**

  ```
  docker compose down
  
  ```

## Testing & Code Coverage

The automated test suite executes directly against an isolated PostgreSQL test database (`hospital_test_db`) inside the container environment without affecting production records.

Run all tests with coverage report:

```
docker compose exec web python -m pytest

```