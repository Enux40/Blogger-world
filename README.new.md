# Blogger-world

A production-ready Django 5 blogging app with user authentication, posts CRUD, profile management, and commenting. Prepared for deployment on Google Cloud Run.

## Features

- User registration, login, logout, profile editing
- Create, read, update, delete blog posts
- Rich text content saved safely (sanitized)
- View posts by user
- Commenting system for authenticated users
- Pagination and Bootstrap styling via crispy-forms

## Local Setup

Prerequisites:
- Python 3.12
- Pip

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Configure environment variables:

Copy `.env.example` to `.env` and fill in values.

3. Apply migrations and create a superuser:

```powershell
python manage.py migrate; python manage.py createsuperuser
```

4. Run the development server:

```powershell
python manage.py runserver
```

## Environment Variables

See `.env.example` for all variables. Key ones:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL` (PostgreSQL URL)
- Email settings: `EMAIL_*`
- `CSRF_TRUSTED_ORIGINS`

## Docker & Cloud Run Deployment

1. Build the Docker image:

```powershell
docker build -t blogger-world:latest .
```

2. Run locally:

```powershell
docker run -e SECRET_KEY=your-secret -e DEBUG=False -e ALLOWED_HOSTS=localhost -e DATABASE_URL=postgres://user:pass@host:5432/db -p 8080:8080 blogger-world:latest
```

3. Deploy to Google Cloud Run (summary):

- Authenticate and set project: `gcloud auth login`; `gcloud config set project <PROJECT_ID>`
- Push image to Artifact Registry or Container Registry
- Deploy:

```powershell
gcloud run deploy blogger-world \ 
  --image=gcr.io/<PROJECT_ID>/blogger-world:latest \ 
  --region=<REGION> \ 
  --allow-unauthenticated \ 
  --set-env-vars=SECRET_KEY=your-secret,DEBUG=False,ALLOWED_HOSTS=your-domain.com,CSRF_TRUSTED_ORIGINS=https://your-domain.com,DATABASE_URL=postgres://user:pass@host:5432/db
```

Ensure Cloud SQL or external database connectivity is configured if using managed Postgres.

## Notes

- Static files are served via WhiteNoise.
- Gunicorn is used as the production WSGI server listening on `0.0.0.0:$PORT`.
