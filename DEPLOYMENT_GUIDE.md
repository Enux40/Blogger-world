# Google Cloud Deployment Checklist

## Pre-Deployment Security Updates

### 1. Update settings.py for Production

```python
import os
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database - Use Cloud SQL in production
if os.environ.get('DATABASE_URL'):
    # Parse DATABASE_URL for Cloud SQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    # Development database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Email configuration using environment variables
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
```

### 2. Create app.yaml for Google App Engine

```yaml
runtime: python312

env_variables:
  SECRET_KEY: "your-new-secret-key-here"
  DEBUG: "False"
  ALLOWED_HOSTS: "your-app-name.appspot.com,your-custom-domain.com"
  EMAIL_HOST_USER: "your-email@gmail.com"
  EMAIL_HOST_PASSWORD: "your-app-password"
  DEFAULT_FROM_EMAIL: "your-email@gmail.com"

handlers:
- url: /static
  static_dir: static/
- url: /media
  static_dir: media/
- url: /.*
  script: auto
```

### 3. Create requirements.txt

```bash
cd /home/runner/work/Blogger-world/Blogger-world
pipenv requirements > requirements.txt
```

Add these additional packages for production:
```
gunicorn
dj-database-url
psycopg2-binary
google-cloud-storage
django-storages
whitenoise
```

### 4. Update .gcloudignore

Create `.gcloudignore` to exclude unnecessary files:
```
.git
.gitignore
*.pyc
__pycache__/
.pytest_cache/
.coverage
htmlcov/
db.sqlite3
media/profile_pics/*
!media/profile_pics/default.jpg
*.log
.env
```

### 5. Configure Static and Media Files

Add to settings.py:
```python
# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files - Use Google Cloud Storage in production
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
```

## Deployment Steps

### 1. Install Google Cloud SDK
```bash
# Follow instructions at https://cloud.google.com/sdk/docs/install
gcloud init
```

### 2. Create Google Cloud Project
```bash
gcloud projects create your-project-id
gcloud config set project your-project-id
```

### 3. Enable Required APIs
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable storage.googleapis.com
```

### 4. Set Up Cloud SQL (Optional but Recommended)
```bash
gcloud sql instances create blogger-db \
    --database-version=POSTGRES_13 \
    --tier=db-f1-micro \
    --region=us-central1

gcloud sql databases create bloggerworld --instance=blogger-db
gcloud sql users set-password postgres --instance=blogger-db --password=YOUR_PASSWORD
```

### 5. Create Cloud Storage Bucket for Media Files
```bash
gsutil mb gs://your-bucket-name
gsutil iam ch allUsers:objectViewer gs://your-bucket-name
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Deploy to Google App Engine
```bash
gcloud app deploy
```

### 9. Run Database Migrations on Production
```bash
gcloud app deploy --promote --version=v1
gcloud app browse
```

## Post-Deployment Testing

### 1. Verify Application
- [ ] Access the deployed URL
- [ ] Check home page loads
- [ ] Test user registration
- [ ] Test user login
- [ ] Test creating a post
- [ ] Test editing a post
- [ ] Test deleting a post
- [ ] Test profile update
- [ ] Test image upload

### 2. Check Logs
```bash
gcloud app logs tail -s default
```

### 3. Monitor Performance
- Visit Cloud Console → App Engine → Dashboard
- Check error rates
- Monitor response times
- Review resource usage

## Security Checklist

- [ ] SECRET_KEY changed from default
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Database password is strong and stored securely
- [ ] Email credentials stored as environment variables
- [ ] HTTPS enforced (App Engine does this by default)
- [ ] CSRF protection enabled (Django default)
- [ ] Static files served securely
- [ ] Media files access controlled

## Rollback Plan

If issues occur:
```bash
# List versions
gcloud app versions list

# Rollback to previous version
gcloud app versions migrate PREVIOUS_VERSION
```

## Environment Variables to Set

Create a `.env.yaml` file (DO NOT commit to git):
```yaml
SECRET_KEY: "your-new-secret-key-here"
DEBUG: "False"
ALLOWED_HOSTS: "your-app-name.appspot.com"
DATABASE_URL: "postgres://user:password@/database?host=/cloudsql/project:region:instance"
EMAIL_HOST_USER: "your-email@gmail.com"
EMAIL_HOST_PASSWORD: "your-app-password"
DEFAULT_FROM_EMAIL: "your-email@gmail.com"
GS_BUCKET_NAME: "your-bucket-name"
```

Then deploy with:
```bash
gcloud app deploy --env-vars-file=.env.yaml
```

## Costs Estimate (Free Tier)

Google Cloud Free Tier includes:
- 28 instance hours per day
- 1 GB Cloud Storage
- 1 GB of egress traffic per day
- 5 GB of Cloud Storage bandwidth

**Recommendation**: Start with free tier and monitor usage.

## Support Resources

- [Google App Engine Python Docs](https://cloud.google.com/appengine/docs/standard/python3)
- [Django on Google Cloud](https://cloud.google.com/python/django)
- [Cloud SQL for Django](https://cloud.google.com/python/django/appengine)

## Notes

1. The application is fully tested and ready for deployment
2. Remember to run `python manage.py migrate` after first deployment
3. Create a superuser to access admin panel: `python manage.py createsuperuser`
4. Consider setting up monitoring and alerting in Google Cloud Console
5. Set up regular database backups
