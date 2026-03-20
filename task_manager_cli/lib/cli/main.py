"""Main CLI entry point.

Separates scripted CLI elements from the business logic encapsulated in TaskService.
"""
import click
from task_manager_cli.lib.services import TaskService

# Initialize the service globally
service = TaskService()


def build_summary_rows(total, completed):
    """Return CLI-friendly summary rows using dicts, tuples, and a list.

    The returned list contains tuples of `(label, value, color)` so the CLI can
    render summary data in a simple, structured way.
    """
    metrics = {
        "Total Tasks": total,
        "Completed Tasks": completed,
        "Pending Tasks": total - completed,
    }
    row_config = [
        ("Total Tasks", None),
        ("Completed Tasks", "green"),
        ("Pending Tasks", "yellow"),
    ]
    return [(label, metrics[label], color) for label, color in row_config]

@click.group()
def cli():
    """Welcome to the Task Manager CLI!
    Use the commands below to manage your tasks efficiently.
    """

@cli.command("list-tasks")
@click.option("--user", help="Filter tasks by user username.")
@click.option("--category", help="Filter tasks by category name.")
def list_tasks_cmd(user, category):
    """List tasks with detailed info and optional filtering."""
    click.echo(f"[*] Querying database... {f'filtering by user:{user}' if user else ''} {f'filtering by category:{category}' if category else ''}")
    
    tasks = service.list_tasks(user_name=user, category_name=category)
    if not tasks:
        click.secho("[-] No tasks found matching your criteria.", fg="yellow")
        return

    click.echo("\n[+] Found the following tasks:")
    for d in tasks:
        # Check if age_days is None and provide a default if it is
        age = d.get('age_days')
        age_str = f"{age} days" if age is not None else "N/A"
        
        details = f"user: {d.get('user', 'None')}, category: {d.get('category', 'None')}"
        status = click.style("DONE", fg="green") if d.get("completed") else click.style("PENDING", fg="red")
        
        click.echo(
            f"  [{d.get('id', '?')}] {d.get('title', 'No Title')} ({details}) - status: {status} - created: {d.get('created', 'Unknown')} - age: {age_str}"
        )

@cli.command("show-summary")
def show_summary_cmd():
    """Show a high-level summary of your productivity."""
    click.echo("[*] Calculating task summary...")
    total, completed = service.get_summary()
    summary_rows = build_summary_rows(total, completed)
    
    click.echo("-" * 30)
    for label, value, color in summary_rows:
        click.secho(f"{label:<16} {value}", fg=color, bold=(label == "Total Tasks"))
    click.echo("-" * 30)

@cli.command("add-task")
@click.argument("title")
@click.option("--desc", help="Optional task description.")
def add_task_cmd(title, desc):
    """Add a new task with validation."""
    try:
        click.echo(f"[*] Attempting to add task: '{title}'...")
        # Simple validation before calling service
        if len(title.strip()) < 3:
            raise click.BadParameter("Title is too short.")
            
        new_task = service.create_task(title=title, description=desc)
        click.secho(f"[✓] Success! Task '{new_task.get('title')}' created with ID: {new_task.get('id')}", fg="green")
    except ValueError as e:
        click.secho(f"[!] Validation Error: {e}", fg="bright_red")
    except Exception as e:
        click.secho(f"[!] An error occurred: {e}", fg="red")

@cli.command("remove-task")
@click.argument("task_id", type=int)
def remove_task_cmd(task_id):
    """Delete a task by its ID."""
    if click.confirm(f"Are you sure you want to delete task #{task_id}?"):
        success = service.delete_task(task_id)
        if success:
            click.secho(f"[✓] Task #{task_id} has been removed.", fg="green")
        else:
            click.secho(f"[-] Task #{task_id} not found.", fg="yellow")

@cli.command("complete-task")
@click.argument("task_id", type=int)
def complete_task_cmd(task_id):
    """Mark a task as completed."""
    success = service.mark_complete(task_id)
    if success:
        click.secho(f"[✓] Task #{task_id} marked as completed.", fg="green")
    else:
        click.secho(f"[-] Task #{task_id} not found.", fg="yellow")

@cli.command("list-users")
def list_users_cmd():
    """List all registered users."""
    users = service.get_users()
    if not users:
        click.echo("No users found.")
        return
    click.echo("\n[+] Registered Users:")
    for u in users:
        click.echo(f"  - {u['username']} ({u['email']})")

@cli.command("list-categories")
@click.option("--user", help="Filter categories by user username.")
def list_categories_cmd(user):
    """List task categories."""
    categories = service.get_categories(user_name=user)
    if not categories:
        click.echo("No categories found.")
        return
    click.echo("\n[+] Categories:")
    for c in categories:
        click.echo(f"  - {c['name']} (Owner: {c['user']})")


@cli.command("interactive")
def interactive_cmd():
    """Run an interactive menu so users can choose different CLI options."""
    menu = {
        "1": "List tasks",
        "2": "Add task",
        "3": "Complete task",
        "4": "Remove task",
        "5": "Show summary",
        "6": "List users",
        "7": "List categories",
        "0": "Exit",
    }

    click.secho("\nTask Manager Interactive Mode", fg="cyan", bold=True)
    while True:
        click.echo("\nChoose an option:")
        for key, label in menu.items():
            click.echo(f"  {key}. {label}")

        choice = click.prompt("Enter your choice", type=str).strip()

        if choice == "1":
            user = click.prompt("Filter by user (optional)", default="", show_default=False).strip() or None
            category = click.prompt("Filter by category (optional)", default="", show_default=False).strip() or None
            ctx = click.get_current_context()
            ctx.invoke(list_tasks_cmd, user=user, category=category)
        elif choice == "2":
            title = click.prompt("Task title").strip()
            desc = click.prompt("Task description (optional)", default="", show_default=False).strip() or None
            ctx = click.get_current_context()
            ctx.invoke(add_task_cmd, title=title, desc=desc)
        elif choice == "3":
            task_id = click.prompt("Task ID to mark complete", type=int)
            ctx = click.get_current_context()
            ctx.invoke(complete_task_cmd, task_id=task_id)
        elif choice == "4":
            task_id = click.prompt("Task ID to remove", type=int)
            ctx = click.get_current_context()
            ctx.invoke(remove_task_cmd, task_id=task_id)
        elif choice == "5":
            ctx = click.get_current_context()
            ctx.invoke(show_summary_cmd)
        elif choice == "6":
            ctx = click.get_current_context()
            ctx.invoke(list_users_cmd)
        elif choice == "7":
            user = click.prompt("Filter by user (optional)", default="", show_default=False).strip() or None
            ctx = click.get_current_context()
            ctx.invoke(list_categories_cmd, user=user)
        elif choice == "0":
            click.secho("Goodbye!", fg="green")
            break
        else:
            click.secho("Invalid option. Please choose one of the menu numbers.", fg="yellow")

def main(argv=None):
    return cli.main(args=argv)

if __name__ == "__main__":
    main()
