# task_manager_cli

Project layout

```
.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
    ├── cli/
    │   └── main.py       <-- CLI entry point
    ├── db/
    │   ├── models.py     <-- SQLAlchemy ORM models
    │   └── seed.py       <-- Database seeding logic
    ├── domain.py         <-- Pure Python domain objects
    ├── services.py       <-- Business logic / Service layer
    ├── debug.py
    └── helpers.py
```

Quickstart

1. Install dependencies (using Pipenv):

```bash
pipenv install --dev
pipenv shell
```

2. Initialize the database and seed demo data:

```bash
python -m task_manager_cli.lib.db.seed
```

3. Run the CLI:

```bash
python -m task_manager_cli.lib.cli.main
```

Run tests:

```bash
pytest task_manager_cli/tests
```

Notes

- **Separation of Concerns**: The project follows a modular architecture:
    - **Models**: [lib/db/models.py](lib/db/models.py) contains pure SQLAlchemy ORM definitions.
    - **Domain**: [lib/domain.py](lib/domain.py) contains plain Python objects used across the application.
    - **Services**: [lib/services.py](lib/services.py) handles the interaction between domain objects and the database.
    - **CLI**: [lib/cli/main.py](lib/cli/main.py) provides the command-line interface using Click.
	
- The canonical code lives under `lib/` per the layout above. Old, scattered modules were consolidated into `lib/` to make the package structure simpler.

Alembic

If you want to manage schema migrations with Alembic, run the following
from the repository root (where `alembic.ini` lives).

Using the project's virtualenv (recommended):

```bash
# activate your virtualenv, then:
alembic upgrade head
```

If you prefer the explicit config path or are running outside the repo
root:

```bash
python -m alembic -c /full/path/to/alembic.ini upgrade head
```

To create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe changes"
```

Note: The project includes a simple initial migration that creates all
tables from `lib/db/models.py`'s `Base.metadata`. For incremental
changes prefer `--autogenerate` so Alembic can produce diffs.
