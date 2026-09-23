# Job Tracker

A full-stack web application to manage, track, and organize job applications.

The project provides a React frontend connected to a FastAPI backend and PostgreSQL database. It supports job application management, searching, filtering, sorting, pagination, statistics, and application-date tracking.

## 🚀 Features

### Job Management

- Add new job applications
- View job applications
- Edit existing job applications
- Delete job applications
- Track application date
- Track application status

### Search & Filtering

- Search jobs by company, role, or location
- Filter jobs by status
- Combine search and status filtering

### Sorting & Pagination

- Sort jobs by company, role, status, or ID
- Sort in ascending or descending order
- Paginate job applications

### Dashboard

- Total job applications
- Applied applications
- Interview applications
- Selected applications
- Rejected applications

### User Experience

- Loading state
- Empty state
- No matching results state
- Error state with retry option
- Responsive design for desktop and mobile

### Backend & Testing

- REST API built with FastAPI
- PostgreSQL database
- SQLAlchemy ORM
- Pydantic validation
- Swagger/OpenAPI documentation
- Automated API testing with pytest
- Separate PostgreSQL test database

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Database

- PostgreSQL

### Testing

- Pytest
- FastAPI TestClient

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
│   ├── .env
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── ...
│
├── screenshots/
│   ├── dashboard-desktop.png
│   └── dashboard-mobile.png
│
├── .gitignore
└── README.md
