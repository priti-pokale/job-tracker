import { useState } from "react"
import "./App.css"

function App() {
  const [showForm, setShowForm] = useState(false)

  const [formData, setFormData] = useState({
    company: "",
    role: "",
    location: "",
    status: "Applied"
  })

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch("http://127.0.0.1:8000/jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error("Failed to create job")
      }

      const data = await response.json()

      console.log("Job created:", data)

      alert("Job added successfully!")

      setFormData({
        company: "",
        role: "",
        location: "",
        status: "Applied"
      })

      setShowForm(false)

    } catch (error) {
      console.error(error)
      alert("Failed to add job")
    }
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
            <p>0</p>
          </div>

          <div className="stat-card">
            <h3>Applied</h3>
            <p>0</p>
          </div>

          <div className="stat-card">
            <h3>Interview</h3>
            <p>0</p>
          </div>

          <div className="stat-card">
            <h3>Selected</h3>
            <p>0</p>
          </div>

          <div className="stat-card">
            <h3>Rejected</h3>
            <p>0</p>
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

          {showForm ? (
            <form className="job-form" onSubmit={handleSubmit}>

              <h3>Add New Job</h3>

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
                <button type="submit" className="save-button">
                    Save Job
                  </button>

                <button
                  className="cancel-button"
                  onClick={() => setShowForm(false)}
                >
                  Cancel
                </button>
              </div>

            </form>
          ) : (
            <div className="empty-state">
              <h3>No jobs yet</h3>
              <p>Add your first job application to get started.</p>
            </div>
          )}

        </section>

      </main>
    </div>
  )
}

export default App