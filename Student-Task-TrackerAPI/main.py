"""Create the FastAPI app and connect its route modules."""


from typing import Optional
from fastapi import FastAPI, HTTPException

from app.database import database_connection, initialize_database
from app.models import TaskInput, TaskUpdateInput

app = FastAPI(title="Student Task Tracker API")


@app.get("/")
def home():
    return {"message": "Welcome! Visit /docs to try the API."}


@app.get("/tasks", summary="List all tasks with optional filtering")
def get_tasks(
    subject: Optional[str] = None,
    status: Optional[str] = None,
):
    result = TaskInput.list_tasks(
        database_connection=database_connection,
        subject=subject,
        status=status,
    )
    return {"tasks": result}


@app.get("/A_tasks/{task_id}", summary="Get a specific task by ID")
def get_task(task_id: int):
    result = TaskInput.get_task(
        task_id=task_id,
        database_connection=database_connection,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": result}


@app.post("/tasks", status_code=201)
def create_task(task: TaskInput):
    result = TaskInput.create_task(
        task_input=task,
        database_connection=database_connection,
    )
    return {"task": result}


@app.patch("/C_tasks/{task_id}", summary="Update a specific task by ID")
def update_task(task_id: int, task_update: TaskUpdateInput):
    existing_task = TaskInput.get_task(
        task_id=task_id,
        database_connection=database_connection,
    )
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True, by_alias=True)

    result = TaskInput.update_task(
        task_id=task_id,
        update_data=update_data,
        database_connection=database_connection,
    )
    return {"task": result}


@app.delete("/D_tasks/{task_id}", summary="Delete a specific task by ID")
def delete_task(task_id: int):
    existing_task = TaskInput.get_task(
        task_id=task_id,
        database_connection=database_connection,
    )
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    TaskInput.delete_task(
        task_id=task_id,
        database_connection=database_connection,
    )
    return {"message": "Task deleted successfully"}


initialize_database()

# uv run dev main:app --reload  