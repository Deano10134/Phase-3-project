"""Main CLI entry point.

Separates scripted CLI elements from the business logic encapsulated in TaskService.
"""
import click
from task_manager_cli.lib.services import TaskService

# Initialize the service globally
service = TaskService()

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
    
    click.echo("-" * 30)
    click.secho(f"Total Tasks:     {total}", bold=True)
    click.secho(f"Completed Tasks: {completed}", fg="green")
    click.secho(f"Pending Tasks:   {total - completed}", fg="yellow")
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

def main(argv=None):
    return cli.main(args=argv)

if __name__ == "__main__":
    main()
