from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Task, Tag
from datetime import datetime, timedelta

# Create engine
engine = create_engine('sqlite:///task_manager.db')
Session = sessionmaker(bind=engine)
session = Session()

def clear_data():
    """Clear all data from tables"""
    session.query(Task).delete()
    session.query(Category).delete()
    session.query(Tag).delete()
    session.query(User).delete()
    session.commit()
    print("✓ Cleared existing data")

def seed_data():
    """Seed the database with sample data"""
    
    # Create users
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com'},
        {'username': 'jane_smith', 'email': 'jane@example.com'},
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        session.add(user)
        users.append(user)
    session.commit()
    print(f"✓ Created {len(users)} users")
    
    # Create categories
    categories_data = [
        {'name': 'Work', 'description': 'Work-related tasks', 'user_id': users[0].id},
        {'name': 'Personal', 'description': 'Personal tasks', 'user_id': users[0].id},
        {'name': 'Shopping', 'description': 'Shopping list items', 'user_id': users[0].id},
        {'name': 'Health', 'description': 'Health and fitness', 'user_id': users[1].id},
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
        {'name': 'urgent', 'color': 'red'},
        {'name': 'important', 'color': 'yellow'},
        {'name': 'quick', 'color': 'green'},
        {'name': 'review', 'color': 'blue'},
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
            'title': 'Complete Phase 3 project',
            'description': 'Build CLI task manager with SQLAlchemy',
            'priority': 3,
            'user_id': users[0].id,
            'category_id': categories[0].id,
            'due_date': datetime.now() + timedelta(days=2)
        },
        {
            'title': 'Review pull requests',
            'description': 'Review team PRs on GitHub',
            'priority': 2,
            'user_id': users[0].id,
            'category_id': categories[0].id,
            'completed': True,
            'completed_at': datetime.now() - timedelta(days=1)
        },
        {
            'title': 'Buy groceries',
            'description': 'Milk, eggs, bread, vegetables',
            'priority': 1,
            'user_id': users[0].id,
            'category_id': categories[2].id,
            'due_date': datetime.now() + timedelta(days=1)
        },
        {
            'title': 'Morning run',
            'description': '5km run in the park',
            'priority': 2,
            'user_id': users[1].id,
            'category_id': categories[3].id,
            'due_date': datetime.now() + timedelta(days=1)
        },
        {
            'title': 'Read book chapter',
            'description': 'Read chapter 5 of Python book',
            'priority': 1,
            'user_id': users[0].id,
            'category_id': categories[1].id,
        },
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        session.add(task)
        tasks.append(task)
    session.commit()
    
    # Add tags to tasks
    tasks[0].tags.extend([tags[0], tags[1]])  # urgent, important
    tasks[1].tags.append(tags[3])  # review
    tasks[2].tags.append(tags[2])  # quick
    tasks[3].tags.append(tags[1])  # important
    
    session.commit()
    print(f"✓ Created {len(tasks)} tasks with tags")
    
    print("\n✅ Database seeded successfully!")

if __name__ == '__main__':
    print("Seeding database...")
    clear_data()
    seed_data()
    session.close()
