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
# from repo root, adjust if manage.py is inside backend/
python manage.py migrate
python manage.py runserver
```

If manage.py is under `backend/`, run `python backend/manage.py` instead.

## Development

- Tests: `python manage.py test`
- Create superuser: `python manage.py createsuperuser`

## Contributing

Create a branch, open a PR, and add tests for new behavior.
