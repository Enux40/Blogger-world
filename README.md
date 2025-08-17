# Django Blogger Web App

A feature-rich blog web application built with Django. This application allows users to create an account, write, edit, and delete their own blog posts, as well as read posts from other users.

## Features

*   **User Authentication:** Users can register for a new account, log in, and log out.
*   **Password Reset:** Users can reset their password via email.
*   **Profile Management:** Users can view and update their profile information, including their username, email, and profile picture.
*   **Blog Post CRUD:** Authenticated users can create, read, update, and delete their own blog posts.
*   **View User's Posts:** Users can view all the posts created by a specific user.
*   **Styled with Bootstrap:** The application uses Bootstrap for a clean and responsive user interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.12 or higher
*   pip
*   pipenv

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Install the dependencies using pipenv:**
    ```bash
    pipenv install
    ```

3.  **Activate the virtual environment:**
    ```bash
    pipenv shell
    ```

4.  **Apply the database migrations:**
    ```bash
    python manage.py migrate
    ```

## Usage

### Running the Development Server

To run the application, use the following command:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

### Running the Tests

To run the test suite, use the following command:

```bash
python manage.py test
```

This will run all the tests for the `blog` and `users` applications.
