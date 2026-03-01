# task_manager_cli

Project layout

```
.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
	├── cli.py
	├── db
	│   ├── models.py
	│   └── seed.py
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
python -m task_manager_cli.lib.cli
```

Run tests:

```bash
pytest task_manager_cli/tests
```

Notes

- The canonical code lives under `lib/` per the layout above. Old, scattered modules were consolidated into `lib/` to make the package structure simpler.
- If you need Alembic migrations, I can add a basic `alembic` setup next.
