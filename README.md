# quizify

Quizify is a robust and scalable Quiz Management application built with Python and the Django framework. It aims to provide a comprehensive platform for creating, managing, and conducting quizzes for employee assessment programs within organizations.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Architecture

![Architecture](https://github.com/IMperiumX/logos/blob/main/quizify/quizify_architecture.png?raw=true)

## Features

**Core Functionality:**

* **User Authentication and Authorization:** Secure user registration, login, and role-based access control (Admin, Quiz Creator, Quiz Taker).
* **Quiz Creation and Management:**
  * Create quizzes with titles, descriptions, and department assignments.
  * Manage quiz status (draft, published, closed).
* **Question Bank and Management:**
  * Create various question types (multiple-choice, true/false, fill-in-the-blank, matching, short answer, essay).
  * Tag questions by topic and difficulty.
  * Randomize question and answer order.
* **Quiz Taking:**
  * User-friendly interface for taking quizzes.
  * Support for timed quizzes.
* **Scoring and Results:**
  * Automatic scoring based on question type.
  * Detailed results tracking (user, quiz, score, date/time).

**Enhanced Functionality:**

* **Department Management:** Assign quizzes and users to departments.
* **User Management:** Admin features for user management (bulk import, department assignment, progress tracking).
* **Feedback Mechanisms:** Options for providing feedback on questions and quizzes.

**Advanced Features (Future):**

* **Reporting and Analytics:** Generate reports on quiz and user performance.
* **API Integrations:** RESTful API (and/or GraphQL API) for integration with other systems (HRIS, LMS).
* **Email Notifications:** Automated email notifications for quiz assignments, reminders, and results.
* **Adaptive Learning:** Dynamically adjust quiz difficulty based on user performance.

## Basic Commands

### Setting Up Your Users

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create a **superuser account**, use this command:

      python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    mypy quizify

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    coverage run -m pytest
    coverage html
    open htmlcov/index.html

#### Running tests with pytest

    pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

### Celery

This app comes with Celery.

To run a celery worker:

    cd quizify
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

    cd quizify
    celery -A config.celery_app beat

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

    cd quizify
    celery -A config.celery_app worker -B -l info

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use [Mailpit](https://github.com/axllent/mailpit) when generating the project a local SMTP server with a web interface will be available.

1. [Download the latest Mailpit release](https://github.com/axllent/mailpit/releases) for your OS.

2. Copy the binary file to the project root.

3. Make it executable:

        chmod +x mailpit

4. Spin up another terminal window and start it there:

        ./mailpit

5. Check out <http://127.0.0.1:8025/> to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

## Deployment

The following details how to deploy this application.
