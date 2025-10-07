# BLOGGER WEB APP
A blog writing and reading web app built with Django.

## Features
- User registration and authentication
- Create, read, update, and delete blog posts
- User profiles with custom profile pictures
- Pagination for blog posts
- Author-only post editing and deletion
- Password reset functionality
- Responsive design with Bootstrap

## Testing Status
✅ **Ready for Deployment**
- 47 automated tests (100% passing)
- 97% code coverage
- All critical bugs fixed

See [TEST_RESULTS.md](TEST_RESULTS.md) for detailed test results.

## Installation

### Prerequisites
- Python 3.12
- Pipenv

### Setup
```bash
# Clone the repository
git clone https://github.com/Enux40/Blogger-world.git
cd Blogger-world

# Install dependencies
pipenv install
pipenv run pip install django-crispy-forms crispy-bootstrap4 Pillow

# Run migrations
pipenv run python manage.py migrate

# Create a superuser (optional)
pipenv run python manage.py createsuperuser

# Run the development server
pipenv run python manage.py runserver
```

Visit http://localhost:8000 to view the application.

## Running Tests
```bash
# Run all tests
pipenv run python manage.py test

# Run tests with coverage
pipenv run coverage run --source='.' manage.py test
pipenv run coverage report
```

## Deployment
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for instructions on deploying to Google Cloud.

## Project Structure
```
Blogger-world/
├── blog/              # Main blog app
│   ├── models.py      # Post model
│   ├── views.py       # Blog views
│   ├── urls.py        # Blog URL patterns
│   └── tests.py       # Blog tests
├── users/             # User management app
│   ├── models.py      # Profile model
│   ├── views.py       # User views
│   ├── forms.py       # User forms
│   └── tests.py       # User tests
├── blog_proj/         # Project settings
│   ├── settings.py    # Django settings
│   └── urls.py        # Main URL patterns
└── manage.py          # Django management script
```

## Technologies Used
- Django 5.0.3
- Bootstrap 4
- Crispy Forms
- Pillow (for image processing)
- SQLite (development)

## License
This project is open source and available for educational purposes.
