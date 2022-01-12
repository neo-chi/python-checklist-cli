from datetime import datetime
from typing import List

import sqlite3

from model import Todo


conn = sqlite3.connect("todos.db")
c = conn.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )"""
    )


def insert_todo(todo: Todo) -> None:
    c.execute("SELECT count(*) FROM todos")
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute(
            "INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)",
            {
                "task": todo.task,
                "category": todo.category,
                "date_added": todo.date_added,
                "date_completed": todo.date_completed,
                "status": todo.status,
                "position": todo.position,
            },
        )


def get_all_todos() -> list[Todo]:
    c.execute("SELECT * FROM todos")
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def delete_todo(position: int) -> None:
    c.execute("SELECT count(*) FROM todos")
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE FROM todos WHERE position = :position", {"position": position})
        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)


def change_position(old_pos: int, new_pos: int, commit=True) -> None:
    c.execute(
        "UPDATE todos SET position = :position_new WHERE position = :position_old",
        {"position_old": old_pos, "position_new": new_pos},
    )

    if commit:
        conn.commit()


def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute(
                """
                UPDATE todos
                SET task = :task, category = :category
                WHERE position = :position
                """,
                {"position": position, "task": task, "category": category},
            )
        elif task is not None:
            c.execute(
                "UPDATE todos SET task = :task, category = :category WHERe position = :position",
                {"position": position, "task": task},
            )
        elif category is not None:
            c.execute(
                "UPDATE todos SET task = :task, category = :category WHERE position = :position",
                {"position": position, "category": category},
            )


def complete_todo(position: int):
    with conn:
        c.execute(
            """
                UPDATE todos
                SET status = 2,
                date_completed = :date_completed
                WHERE position = :position
                """,
            {"position": position, "date_completed": datetime.now().isoformat()},
        )
