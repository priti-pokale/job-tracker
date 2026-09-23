import { useEffect, useState } from "react"
import "./App.css"

function App() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [showForm, setShowForm] = useState(false)
  const [editingJob, setEditingJob] = useState(null)
  const [search, setSearch] = useState("")
  const [statusFilter, setStatusFilter] = useState("")
  const [sortBy, setSortBy] = useState("id")
  const [sortOrder, setSortOrder] = useState("asc")
  const [page, setPage] = useState(1)
  const jobsPerPage = 10
  const [stats, setStats] = useState({
  total: 0,
  applied: 0,
  interview: 0,
  selected: 0,
  rejected: 0
})

  useEffect(() => {
  const params = new URLSearchParams()

  params.append(
    "skip",
    String((page - 1) * jobsPerPage)
  )

  params.append(
    "limit",
    String(jobsPerPage)
  )

  if (search.trim() !== "") {
    params.append("search", search)
  }

  if (statusFilter !== "") {
    params.append("status", statusFilter)
  }

  params.append("sort_by", sortBy)
  params.append("order", sortOrder)


  fetch(`http://127.0.0.1:8000/jobs?${params.toString()}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch jobs")
      }

      return response.json()
    })
    .then((data) => {
      setJobs(data)
      setLoading(false)
    })
    .catch((error) => {
      console.error(error)
      setError("Failed to load jobs")
      setLoading(false)
    })
  }, [search, statusFilter, page])

  useEffect(() => {
  setPage(1)
  }, [search, statusFilter, sortBy, sortOrder, page])

  useEffect(() => {
  fetch("http://127.0.0.1:8000/jobs/stats")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch statistics")
      }

      return response.json()
    })
    .then((data) => {
  console.log("Stats:", data)
  setStats(data)
})
    .catch((error) => {
      console.error(error)
    })
  }, [])

  const [formData, setFormData] = useState({
    company: "",
    role: "",
    location: "",
    status: "Applied",
    applied_date: ""
  })

  const handleSubmit = async (e) => {
  e.preventDefault()

  try {
    console.log("Form data being sent:", formData)
    let response

    if (editingJob) {
      // Update existing job
      response = await fetch(
        `http://127.0.0.1:8000/jobs/${editingJob.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(formData)
        }
      )
    } else {
      // Create new job
      response = await fetch(
        "http://127.0.0.1:8000/jobs",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(formData)
        }
      )
    }

    if (!response.ok) {
      throw new Error("Failed to save job")
    }

    const data = await response.json()

    if (editingJob) {
      // Replace the old job with updated job
      setJobs((previousJobs) =>
        previousJobs.map((job) =>
          job.id === data.id ? data : job
        )
      )

      alert("Job updated successfully!")
    } else {
      // Add new job to list
      setJobs((previousJobs) => [
        ...previousJobs,
        data
      ])

      alert("Job added successfully!")
    }

    // Reset form
    setFormData({
      company: "",
      role: "",
      location: "",
      status: "Applied",
      applied_date: ""
    })

    setEditingJob(null)
    setShowForm(false)

  } catch (error) {
    console.error(error)
    alert("Failed to save job")
  }
}

  const handleDelete = async (jobId) => {
  const confirmed = window.confirm(
    "Are you sure you want to delete this job?"
  )

  if (!confirmed) {
    return
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/jobs/${jobId}`,
      {
        method: "DELETE"
      }
    )

    if (!response.ok) {
      throw new Error("Failed to delete job")
    }

    setJobs((previousJobs) =>
      previousJobs.filter((job) => job.id !== jobId)
    )

    alert("Job deleted successfully!")
  } catch (error) {
    console.error(error)
    alert("Failed to delete job")
  }
}

  const handleEdit = (job) => {
  setEditingJob(job)

  setFormData({
    company: job.company,
    role: job.role,
    location: job.location,
    status: job.status,
    applied_date: job.applied_date || ""
  })

  setShowForm(true)
}

  return (
    <div className="app">

      <header className="header">
        <h1>Job Tracker</h1>
        <p>Track your job applications easily</p>
      </header>

      <main className="dashboard">

        <section className="stats">

          <div className="stat-card">
            <h3>Total Jobs</h3>
            <p>{stats.total}</p>
          </div>

          <div className="stat-card">
            <h3>Applied</h3>
            <p>{stats.applied}</p>
          </div>

          <div className="stat-card">
            <h3>Interview</h3>
            <p>{stats.interview}</p>
          </div>

          <div className="stat-card">
            <h3>Selected</h3>
            <p>{stats.selected}</p>
          </div>

          <div className="stat-card">
            <h3>Rejected</h3>
            <p>{stats.rejected}</p>
          </div>

        </section>

        <section className="jobs-section">

          <div className="section-header">
            <h2>My Job Applications</h2>

            <button
              className="add-button"
              onClick={() => setShowForm(true)}
            >
              + Add Job
            </button>
          </div>

          <div className="filters">

            <input
              type="text"
              placeholder="Search company, role or location..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All Status</option>
              <option value="Applied">Applied</option>
              <option value="Interview">Interview</option>
              <option value="Selected">Selected</option>
              <option value="Rejected">Rejected</option>
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="id">Sort By ID</option>
              <option value="company">Sort By Company</option>
              <option value="role">Sort By Role</option>
              <option value="status">Sort By Status</option>
            </select>

            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>

          </div>

          {showForm ? (
            <form className="job-form" onSubmit={handleSubmit}>

              <h3>{editingJob ? "Edit Job" : "Add New Job"}</h3>

              <div className="form-group">
                <label>Company</label>
                <input
                  type="text"
                  placeholder="e.g. Google"
                  value={formData.company}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      company: e.target.value
                    })
                  }
                />
              </div>

              <div className="form-group">
                <label>Role</label>
                <input
                  type="text"
                  placeholder="e.g. Python Developer"
                  value={formData.role}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      role: e.target.value
                    })
                  }
                />
              </div>

              <div className="form-group">
                <label>Location</label>
                <input
                  type="text"
                  placeholder="e.g. Pune"
                  value={formData.location}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      location: e.target.value
                    })
                  }
                />
              </div>

              <div className="form-group">
                <label>Application Date</label>

                <input
                  type="date"
                  value={formData.applied_date}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      applied_date: e.target.value
                    })
                  }
                />
              </div>

              <div className="form-group">
                <label>Status</label>

                <select
                  value={formData.status}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      status: e.target.value
                    })
                  }
                >
                  <option value="Applied">Applied</option>
                  <option value="Interview">Interview</option>
                  <option value="Selected">Selected</option>
                  <option value="Rejected">Rejected</option>
                </select>
              </div>

              <div className="form-actions">

                <button
                  type="submit"
                  className="save-button"
                >
                  {editingJob ? "Update Job" : "Save Job"}
                </button>

                <button
                  type="button"
                  className="cancel-button"
                  onClick={() => setShowForm(false)}
                >
                  Cancel
                </button>

              </div>

            </form>
          ) : (
            <>
              {loading && (
                <div className="empty-state">
                  <h3>Loading jobs...</h3>
                  <p>Please wait while we fetch your applications.</p>
                </div>
              )}

              {error && (
                <div className="empty-state">
                  <h3>Something went wrong</h3>
                  <p>{error}</p>

                  <button
                    className="add-button"
                    onClick={() => window.location.reload()}
                  >
                    Try Again
                  </button>
                </div>
              )}

              {!loading && !error && jobs.length === 0 && (
                <div className="empty-state">
                  {search || statusFilter ? (
                    <>
                      <h3>No matching jobs found</h3>
                      <p>
                        Try changing your search or status filter.
                      </p>
                    </>
                  ) : (
                    <>
                      <h3>No jobs added yet</h3>
                      <p>
                        Start tracking your job applications by adding your first job.
                      </p>
                    </>
                  )}
                </div>
              )}

              {!loading && !error && jobs.length > 0 && (
  <>
    <div className="jobs-list">
      {jobs
        .map((job) => (
          <div className="job-card" key={job.id}>

            <div>
              <h3>{job.company}</h3>
              <p>{job.role}</p>
              <span>{job.location}</span>

              {job.applied_date && (
                <p className="applied-date">
                  Applied: {job.applied_date}
                </p>
              )}
            </div>

            <div className="job-actions">

              <span className="job-status">
                {job.status}
              </span>

              <button
                className="edit-button"
                onClick={() => handleEdit(job)}
              >
                Edit
              </button>

              <button
                className="delete-button"
                onClick={() => handleDelete(job.id)}
              >
                Delete
              </button>

            </div>

          </div>
        ))}
    </div>

    <div className="pagination">

      <button
        onClick={() => setPage(page - 1)}
        disabled={page === 1}
      >
        Previous
      </button>

      <span>Page {page}</span>

      <button
        onClick={() => setPage(page + 1)}
        disabled={jobs.length < jobsPerPage}
      >
        Next
      </button>

    </div>
  </>
)}
            </>
          )}

        </section>

      </main>
    </div>
  )
}

export default App