# Job Tracker API

A REST API built with FastAPI and PostgreSQL to manage and track job applications.

## 🚀 Features

- Create job applications
- Get all job applications
- Get a job by ID
- Update a complete job application
- Partially update a job application
- Delete job applications
- Filter jobs by status
- Filter jobs by company
- Filter jobs by role
- Search jobs by company, role, or location
- Pagination
- Sorting
- Job application statistics
- Swagger/OpenAPI documentation
- Automated API testing with pytest
- Separate PostgreSQL test database

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest
- Uvicorn

## 📁 Project Structure

```text
job-tracker/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── test_main.py
│   ├── requirements.txt
│   └── .env
│
├── .gitignore
└── README.md