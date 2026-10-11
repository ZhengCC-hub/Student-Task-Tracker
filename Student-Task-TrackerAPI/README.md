Student Task Tracker API

A lightweight RESTful API built with FastAPI, SQLite, and Pydantic to help students manage, track, and filter their academic assignments and tasks. Managed using uv and organized with a standard Python src package layout.🛠️ Project FeaturesTask Management (CRUD): Create, retrieve, update, and delete assignment records.   Query Filtering: Search tasks by subject or status (e.g., pending vs. in-progress).   Partial Updates: Modify specific fields using dynamic PATCH requests.   Data Validation: Automatic payload validation for mandatory titles, subjects, due dates, and default priority levels.   Interactive API Docs: Built-in Swagger UI testing interface generated automatically by FastAPI.   


Getting StartedPrerequisitesEnsure you have Python 3.12+ and uv installed on your system.InstallationClone or open the project folder:PowerShellcd Assignment-Tracker

Set up the virtual environment and sync dependencies:PowerShelluv sync
Running the API ServerRun the development server with auto-reload using uv:PowerShelluv run uvicorn assignment_tracker.app.main:app --reload --app-dir src

Once started, access the server at:Base URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)Interactive Docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

API Endpoint Reference
1. Root / WelcomeGET /Purpose: Returns a simple welcome message and directs users to the API documentation.
   
2. List Tasks (With Filtering)GET /tasks   Purpose: Retrieves all task records from Tracker.db.   Query Parameters:subject (optional, string): Filter tasks by course/subject (case-insensitive).   status (optional, string): Filter tasks by completion status.   Example Request:GET /tasks?subject=Math&status=in-progress
   
3. Retrieve Single TaskGET /Get_tasks/{task_id}   Purpose: Fetches full details for a single task matching the given ID.   Path Parameters:task_id (integer, required)

4. Create TaskPOST /Create_tasks   Purpose: Inserts a new task record into the database. Automatically sets the initial status to "in-progress".   Request Body (JSON):JSON{
  "title": "Finish Calculus Homework",
  "subject": "Mathematics",
  "dueDate": "2026-10-15",
  "priority": "High"
}
(Note: priority is optional and defaults to "Medium")   5. Update Task (Partial)PATCH /Upd_tasks/{task_id}   Purpose: Performs a partial update on specific fields without needing to resend unchanged data.   Path Parameters:task_id (integer, required)   Request Body (JSON):JSON{
  "status": "completed",
  "priority": "Low"
}
6. Delete TaskDELETE /Del_tasks/{task_id}   Purpose: Permanently deletes a task record from the database by ID.   Path Parameters:task_id (integer, required)
