from datetime import datetime, timedelta

from .models import Base, User, Category, Task, Tag, task_tag
from .session import get_engine, get_session


def seed_database(engine=None, num_users=2, num_tasks=5):
    """Seed the database with sample data"""
    engine = engine or get_engine()
    Base.metadata.create_all(engine)  # Create tables
    session = get_session(engine)
    try:
        clear_data(session)
        seed_data(session, num_users=num_users, num_tasks=num_tasks)
        print("\n✅ Database seeded successfully!")
    finally:
        session.close()


def clear_data(session):
    """Clear all data from tables"""
    session.execute(task_tag.delete())
    session.query(Task).delete()
    session.query(Category).delete()
    session.query(Tag).delete()
    session.query(User).delete()
    session.commit()
    print("✓ Cleared existing data")


def seed_data(session, num_users, num_tasks):
    """Seed the database with sample data"""

    # Create users
    users_data = [
        {"username": "john_doe", "email": "john@example.com"},
        {"username": "jane_smith", "email": "jane@example.com"},
    ]

    users = []
    for user_data in users_data[:num_users]:
        user = User(**user_data)
        session.add(user)
        users.append(user)
    session.commit()
    print(f"✓ Created {len(users)} users")

    if not users:
        return

    # Create categories
    categories_data = [
        {"name": "Work", "description": "Work-related tasks", "user": users[0]},
        {"name": "Personal", "description": "Personal tasks", "user": users[0]},
        {
            "name": "Shopping",
            "description": "Shopping list items",
            "user": users[0],
        },
        {"name": "Health", "description": "Health and fitness", "user": users[-1]},
    ]

    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        session.add(category)
        categories.append(category)
    session.commit()
    print(f"✓ Created {len(categories)} categories")

    # Create tags
    tags_data = [
        {"name": "urgent", "color": "red"},
        {"name": "important", "color": "yellow"},
        {"name": "quick", "color": "green"},
        {"name": "review", "color": "blue"},
    ]

    tags = []
    for tag_data in tags_data:
        tag = Tag(**tag_data)
        session.add(tag)
        tags.append(tag)
    session.commit()
    print(f"✓ Created {len(tags)} tags")

    # Create tasks
    tasks_data = [
        {
            "title": "Complete Phase 3 project",
            "description": "Build CLI task manager with SQLAlchemy",
            "priority": 3,
            "user": users[0],
            "category": categories[0],
            "due_date": datetime.now() + timedelta(days=2),
        },
        {
            "title": "Review pull requests",
            "description": "Review team PRs on GitHub",
            "priority": 2,
            "user": users[0],
            "category": categories[0],
            "completed": True,
            "completed_at": datetime.now() - timedelta(days=1),
        },
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, vegetables",
            "priority": 1,
            "user": users[0],
            "category": categories[2],
            "due_date": datetime.now() + timedelta(days=1),
        },
        {
            "title": "Morning run",
            "description": "5km run in the park",
            "priority": 2,
            "user": users[-1],
            "category": categories[3],
            "due_date": datetime.now() + timedelta(days=1),
        },
        {
            "title": "Read book chapter",
            "description": "Read chapter 5 of Python book",
            "priority": 1,
            "user": users[0],
            "category": categories[1],
        },
    ]

    tasks = []
    for task_data in tasks_data[:num_tasks]:
        task = Task(**task_data)
        session.add(task)
        tasks.append(task)
    session.commit()

    # Add tags to tasks
    if tasks:
        tasks[0].tags.extend([tags[0], tags[1]])  # urgent, important
    if len(tasks) > 1:
        tasks[1].tags.append(tags[3])  # review
    if len(tasks) > 2:
        tasks[2].tags.append(tags[2])  # quick
    if len(tasks) > 3:
        tasks[3].tags.append(tags[1])  # important

    session.commit()
    print(f"✓ Created {len(tasks)} tasks with tags")


if __name__ == "__main__":
    print("Seeding database...")
    seed_database()
