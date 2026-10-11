# Student Task Tracker API

A lightweight RESTful API built with FastAPI, SQLite, and Pydantic to help students manage, track, and filter their academic assignments and tasks. Managed using uv and organized with a standard Python src package layout.

---

## Project Features

* **Task Management (CRUD):** Create, retrieve, update, and delete assignment records.
* **Query Filtering:** Search tasks by subject or status (e.g., pending vs. in-progress).
* **Partial Updates:** Modify specific fields using dynamic PATCH requests.
* **Data Validation:** Automatic payload validation for mandatory titles, subjects, due dates, and default priority levels.
* **Interactive API Docs:** Built-in Swagger UI testing interface generated automatically by FastAPI.

---

## Getting Started

### Prerequisites

Ensure you have Python 3.12+ and uv installed on your system.

### Installation

Clone or open the project folder:

```powershell
cd Assignment-Tracker

Running the API Server
Run the development server with auto-reload using uv:
uv run dev main:app --reload  
