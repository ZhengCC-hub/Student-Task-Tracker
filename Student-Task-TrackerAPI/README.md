# Student Task Tracker API

A REST API built with FastAPI & SQLite to manage student assignments, tasks, and deadlines.

## Features

* Manage tasks and assignments (create, read, update, delete)
* Search and filter tasks by subject or status
* Perform partial task updates dynamically using PATCH requests
* Automatic input validation via Pydantic for titles, subjects, due dates, and priority levels

---

## 1. Requirements

* Python 3.10 or newer (check with `python --version`, or `py --version` on Windows)
* Git
* No database server is needed: SQLite is built into Python.

---

## 2. Setup

### 2.1 Clone the repository

```powershell
git clone [https://github.com/ZhengCC-hub/Student-Task-Tracker.git](https://github.com/ZhengCC-hub/Student-Task-Tracker.git)
cd Student-Task-Tracker/StudentTaskTrackerAPI
```

### 2.2 Create and activate a virtual environment

Run the commands for your system from inside the project folder:

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If PowerShell refuses to run the activation script, run this once and try again:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**macOS / Linux (bash or zsh)**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

When it works, your prompt starts with `(.venv)`.

### 2.3 Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2.4 Run the application

```powershell
uvicorn main:app --reload
```

You should see a line like `Uvicorn running on http://127.0.0.1:8000`. Press `Ctrl+C` to stop it.

### 2.5 Open the interactive documentation

Open http://127.0.0.1:8000/docs in a browser. This Swagger page lists every endpoint and lets you test them without writing any client code.

### 2.6 The database

The first time the app starts, it connects to a SQLite file. Data is kept between restarts.

To start again from an empty database: stop the server, delete the database file, and start the server again. Do this before running tests so the IDs in the examples match yours.

---

## 3. Using the API

On the `/docs` page, click an endpoint, press **Try it out**, edit the request body or fill in the parameters, then press **Execute**. The result appears under *Server response*. Errors come back as `{"detail": "..."}` with a message explaining what went wrong.

---

## 4. Project structure

```text
Student-Task-TrackerAPI/
├── app/
│   ├── __init__.py
│   ├── database.py          # SQLite database connection handler
│   └── models.py            # Pydantic models & data validation
├── main.py                  # FastAPI app initialization and route definitions
├── README.md                # Project documentation
└── requirements.txt         # Project dependencies list
```

---

## 5. Sample tests for every endpoint

Do the tests in order, starting from an empty database (see section 2.6). Part A covers the normal flow, and Part B covers error cases and validation rules.

### Part A: Normal flow

#### A1. Home
* `GET /`
  * Returns `{"message": "Welcome! Visit /docs to try the API."}`

#### A2. List Tasks (With Filtering)
* `GET /tasks`
  * Returns an empty array `[]` initially.

#### A3. Create Tasks
* Create a task: `POST /Create_tasks`
  ```json
  {
    "title": "Finish Calculus Homework",
    "subject": "Mathematics",
    "dueDate": "2026-10-15",
    "priority": "High"
  }
  ```
  * Comes back with `id: 1` and status `"in-progress"`.

* Create a second task: `POST /Create_tasks`
  ```json
  {
    "title": "Read Physics Chapter 3",
    "subject": "Physics",
    "dueDate": "2026-10-18"
  }
  ```
  * Comes back with `id: 2`, status `"in-progress"`, and priority `"Medium"` (default).

#### A4. Retrieve Tasks
* Get all tasks: `GET /tasks`
  * Returns both tasks.
* Filter by subject: `GET /tasks?subject=physics`
  * Returns item 2 only.
* Get specific task: `GET /Get_tasks/1`
  * Returns "Finish Calculus Homework".

#### A5. Update Task
* Partial update: `PATCH /Upd_tasks/1`
  ```json
  {
    "status": "completed",
    "priority": "Low"
  }
  ```
  * Returns task 1 with updated status `"completed"` and priority `"Low"`.

#### A6. Delete Task
* `DELETE /Del_tasks/2`
* Retrieve task 2 again: `GET /Get_tasks/2` reports `404 Not Found`.

---

### Part B: Error cases to try

Run these after Part A. Each request should be rejected as shown.

#### Input Validation Errors

| Request | Change / Payload | Expected Result |
| :--- | :--- | :--- |
| `POST /Create_tasks` | `{"title": "", "subject": "Math", "dueDate": "2026-10-15"}` | Validation Error (title must be at least 1 character) |
| `POST /Create_tasks` | `{"title": "Homework"}` | Validation Error (subject and dueDate are required) |
| `GET /Get_tasks/{task_id}` | `99` | `404 Task not found` |
| `GET /Get_tasks/{task_id}` | `abc` | Validation Error (`task_id` must be an integer) |
| `PATCH /Upd_tasks/{task_id}` | `99` with `{"status": "completed"}` | `404 Task not found` |
| `DELETE /Del_tasks/{task_id}` | `99` | `404 Task not found` |
