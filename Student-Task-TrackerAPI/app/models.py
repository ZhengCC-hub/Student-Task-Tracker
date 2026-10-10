"""Data models used to validate API input and output."""

from typing import Optional
from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    """Fields required when creating a task record."""

    title: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    due_date: str = Field(alias="dueDate")
    priority: Optional[str] = Field(default="Medium")

    @staticmethod
    def list_tasks(database_connection, subject: Optional[str] = None, status: Optional[str] = None):
        """Fetch tasks with optional subject and status query filters."""
        query = "SELECT id, title, subject, due_date AS dueDate, priority, status FROM tasks WHERE 1=1"
        params = []

        if subject:
            query += " AND LOWER(subject) = LOWER(?)"
            params.append(subject)
        if status:
            query += " AND LOWER(status) = LOWER(?)"
            params.append(status)

        query += " ORDER BY id"

        with database_connection() as connection:
            rows = connection.execute(query, params).fetchall()
        # Convert sqlite3.Row objects to standard python dictionaries
        return [dict(row) for row in rows]

    @staticmethod
    def create_task(task_input, database_connection):
        """Insert a new task into the database."""
        with database_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, subject, due_date, priority, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task_input.title,
                    task_input.subject,
                    task_input.due_date,
                    task_input.priority,
                    "in-progress",
                ),
            )
            row = connection.execute(
                """
                SELECT id, title, subject, due_date AS dueDate, priority, status
                FROM tasks WHERE id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_task(task_id: int, database_connection):
        """Fetch a single task by ID."""
        with database_connection() as connection:
            row = connection.execute(
                """
                SELECT id, title, subject, due_date AS dueDate, priority, status
                FROM tasks WHERE id = ?
                """,
                (task_id,),
            ).fetchone()
        return dict(row) if row else None

    @staticmethod
    def update_task(task_id: int, update_data: dict, database_connection):
        """Perform a partial update (PATCH) on a task dynamically."""
        if not update_data:
            return TaskInput.get_task(task_id, database_connection)

        db_fields = []
        params = []

        for key, value in update_data.items():
            db_key = "due_date" if key == "dueDate" else key
            db_fields.append(f"{db_key} = ?")
            params.append(value)

        params.append(task_id)
        set_clause = ", ".join(db_fields)

        with database_connection() as connection:
            connection.execute(
                f"UPDATE tasks SET {set_clause} WHERE id = ?",
                params,
            )
            row = connection.execute(
                """
                SELECT id, title, subject, due_date AS dueDate, priority, status
                FROM tasks WHERE id = ?
                """,
                (task_id,),
            ).fetchone()
        return dict(row) if row else None

    @staticmethod
    def delete_task(task_id: int, database_connection):
        """Delete a task by ID."""
        with database_connection() as connection:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))


class TaskUpdateInput(BaseModel):
    """Fields allowed for partial updates via PATCH /tasks/{id}."""

    title: Optional[str] = Field(default=None, min_length=1)
    subject: Optional[str] = Field(default=None, min_length=1)
    due_date: Optional[str] = Field(default=None, alias="dueDate")
    priority: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)