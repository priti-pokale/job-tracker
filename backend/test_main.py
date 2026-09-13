from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API is running!"
    }


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "company": "Google",
            "role": "Python Developer",
            "location": "Pune",
            "status": "Applied"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Google"
    assert data["role"] == "Python Developer"
    assert data["location"] == "Pune"
    assert data["status"] == "Applied"


def test_get_jobs():
    response = client.get("/jobs")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_filter_by_status():
    response = client.get("/jobs?status=Applied")

    assert response.status_code == 200

    data = response.json()

    for job in data:
        assert job["status"] == "Applied"

def test_filter_by_company():
    response = client.get("/jobs?company=Google")

    assert response.status_code == 200

    data = response.json()

    for job in data:
        assert "google" in job["company"].lower()

def test_filter_by_role():
    response = client.get("/jobs?role=Python")

    assert response.status_code == 200

    data = response.json()

    for job in data:
        assert "python" in job["role"].lower()

def test_filter_by_company_and_role():
    response = client.get(
        "/jobs?company=Google&role=Python"
    )

    assert response.status_code == 200

    data = response.json()

    for job in data:
        assert "google" in job["company"].lower()
        assert "python" in job["role"].lower()

def test_pagination():
    response = client.get("/jobs?skip=0&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 2

def test_sorting():
    response = client.get("/jobs?sort_by=company&order=asc")

    assert response.status_code == 200

    data = response.json()

    companies = [job["company"] for job in data]

    assert companies == sorted(companies, key=str.lower)

def test_patch_job():
    # First create a job
    create_response = client.post(
        "/jobs",
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "location": "Pune",
            "status": "Applied"
        }
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["id"]

    # Update only the status
    response = client.patch(
        f"/jobs/{job_id}",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Interview"
    assert data["company"] == "Microsoft"
    assert data["role"] == "Backend Developer"
    assert data["location"] == "Pune"

def test_update_job():
    # Create a job first
    create_response = client.post(
        "/jobs",
        json={
            "company": "Amazon",
            "role": "Developer",
            "location": "Pune",
            "status": "Applied"
        }
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["id"]

    # Update the complete job
    response = client.put(
        f"/jobs/{job_id}",
        json={
            "company": "Amazon",
            "role": "Senior Python Developer",
            "location": "Bangalore",
            "status": "Interview"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Amazon"
    assert data["role"] == "Senior Python Developer"
    assert data["location"] == "Bangalore"
    assert data["status"] == "Interview"

def test_delete_job():
    # Create a job first
    create_response = client.post(
        "/jobs",
        json={
            "company": "TCS",
            "role": "Python Developer",
            "location": "Pune",
            "status": "Applied"
        }
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["id"]

    # Delete the job
    response = client.delete(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job deleted successfully"
    }

    # Confirm the job no longer exists
    get_response = client.get(f"/jobs/{job_id}")

    assert get_response.status_code == 404

def test_job_stats():
    response = client.get("/jobs/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "applied" in data
    assert "interview" in data
    assert "rejected" in data
    assert "selected" in data

def test_update_nonexistent_job():
    response = client.put(
        "/jobs/999999",
        json={
            "company": "Test",
            "role": "Developer",
            "location": "Pune",
            "status": "Applied"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_patch_nonexistent_job():
    response = client.patch(
        "/jobs/999999",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_delete_nonexistent_job():
    response = client.delete("/jobs/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"