# mnhs-ai-forms-system

Django-based backend for managing forms, submissions, approvals, and analytics.

## Getting started

These are minimal steps to run the backend locally. Adjust Python version and database settings as needed.

Prerequisites:
- Python 3.11
- PostgreSQL (or set DATABASE_URL to a Sqlite URL for quick testing)

Clone and prepare virtualenv

```bash
git clone https://github.com/mharcadayong/Mnhs-ai-forms-system.git
cd Mnhs-ai-forms-system
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Environment

Create a `.env` file based on `.env.example` and set required variables:

- DJANGO_SECRET_KEY
- DEBUG (True/False)
- DATABASE_URL (e.g. postgres://user:pass@localhost:5432/dbname)
- ALLOWED_HOSTS (comma separated)

Run migrations and start

```bash
# If a Django manage.py exists at the repository root:
python manage.py migrate
python manage.py runserver

# If manage.py is inside the `backend/` package, run:
python backend/manage.py migrate
python backend/manage.py runserver
```

I inspected the repository and could not find a top-level `manage.py` file. If your Django project entrypoint lives in a different path, replace the command above with the correct relative path (for example `python path/to/manage.py ...`). If you don't yet have a `manage.py`, you can create one by running `django-admin startproject <project_name> .` from within the `backend/` directory and moving the apps into the created project.

Settings module

If your project uses a custom settings module, set the `DJANGO_SETTINGS_MODULE` environment variable or edit `manage.py` to point at the correct settings. Example:

```bash
export DJANGO_SETTINGS_MODULE=backend.settings
```

## Development

- Tests: `python manage.py test` (or `python backend/manage.py test`)
- Create superuser: `python manage.py createsuperuser`

## Contributing

Create a branch, open a PR, and add tests for new behavior.
