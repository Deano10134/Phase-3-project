from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between Task and Tag
task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')
    categories = relationship('Category', back_populates='user', cascade='all, delete-orphan')
    
    # Python logic applied to columns
    @hybrid_property
    def task_count(self):
        return len(self.tasks)
    
    @hybrid_property
    def completed_task_count(self):
        return len([task for task in self.tasks if task.completed])
    
    def completion_rate(self):
        """Calculate percentage of completed tasks"""
        if not self.tasks:
            return 0.0
        return (self.completed_task_count / self.task_count) * 100
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        """Convert to dictionary for CLI display"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'task_count': self.task_count,
            'completed_tasks': self.completed_task_count,
            'completion_rate': f"{self.completion_rate():.1f}%"
        }


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship('User', back_populates='categories')
    tasks = relationship('Task', back_populates='category')
    
    @hybrid_property
    def task_count(self):
        return len(self.tasks)
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description or 'No description',
            'task_count': self.task_count,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)  # 1=Low, 2=Medium, 3=High
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship('User', back_populates='tasks')
    category = relationship('Category', back_populates='tasks')
    tags = relationship('Tag', secondary=task_tags, back_populates='tasks')
    
    # Python logic applied to columns
    @hybrid_property
    def is_overdue(self):
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False
    
    @hybrid_property
    def priority_label(self):
        labels = {1: 'Low', 2: 'Medium', 3: 'High'}
        return labels.get(self.priority, 'Unknown')
    
    @hybrid_property
    def status(self):
        if self.completed:
            return 'Completed'
        elif self.is_overdue:
            return 'Overdue'
        else:
            return 'Pending'
    
    def mark_complete(self):
        """Mark task as completed with timestamp"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
    
    def to_dict(self):
        """Convert to dictionary for CLI display"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or 'No description',
            'status': self.status,
            'priority': self.priority_label,
            'category': self.category.name if self.category else 'Uncategorized',
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else 'No due date',
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M') if self.completed_at else 'N/A'
        }


class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String, default='default')
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    tasks = relationship('Task', secondary=task_tags, back_populates='tags')
    
    @hybrid_property
    def task_count(self):
        return len(self.tasks)
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'task_count': self.task_count,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }