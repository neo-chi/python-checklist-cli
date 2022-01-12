import typer
from rich.console import Console
from rich.table import Table

from model import Todo
import database

console = Console()


app = typer.Typer()


@app.command(short_help="Adds a task")
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    database.insert_todo(todo)
    show()


@app.command(short_help="Deletes an item")
def delete(position: int):
    typer.echo(f"deleting {position}")
    # NOTE: indices in UI begin at 1, but in database at 0.
    database.delete_todo(position - 1)
    show()


@app.command(short_help="Edits a task")
def update(position: int, task: str = None, category: str = None):
    typer.echo(f"updating {position}")
    database.update_todo(position, task, category)
    show()


@app.command(short_help="Complete an item")
def complete(position: int):
    typer.echo(f"complete {position}")
    database.complete_todo(position - 1)
    show()


@app.command(short_help="Show the task list table")
def show():
    tasks = database.get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "❓")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {"LEARN": "cyan", "YOUTUBE": "red", "Craft": "cyan", "Gather": "green"}
        # if category in colors:
        #     return COLOR[category]
        # return 'white'
        return COLORS[category] if category in COLORS else "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(str(idx), task.task, f"[{c}]{task.category}[/{c}]", is_done_str)
    console.print(table)


def main():
    database.create_table()
    app()


if __name__ == "__main__":
    main()
