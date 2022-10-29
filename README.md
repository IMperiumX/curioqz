Curioqz
====

A Quiz Management application aims at the Employee assessment programs carried out in the organization by conducting Quizzes. The application focuses on creating a well defined exam/quiz for individual departments.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/pydanny/cookiecutter-django/)

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License

:   GPLv3

Project Preview
===============

![Langing Page](./assets/landing.png)

![students and Professor Login](./assets/users.png)

Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you\'ll see a \"Verify Your E-mail
    Address\" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user\'s email should be verified and ready to go.

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy quiz

### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with py.test

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS
compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Celery

This app comes with Celery.

To run a celery worker:

``` {.bash}
cd quiz
celery -A config.celery_app worker -l info
```

Please note: For Celery\'s import magic to work, it is important *where*
the celery commands are run. If you are in the same folder with
*manage.py*, you should be right.

### Email Server

In development, it is often nice to be able to see emails that are being
sent from your application. If you choose to use
[MailHog](https://github.com/mailhog/MailHog) when generating the
project a local SMTP server with a web interface will be available.

1.  [Download the latest MailHog
    release](https://github.com/mailhog/MailHog/releases) for your OS.

2.  Rename the build to `MailHog`.

3.  Copy the file to the project root.

4.  Make it executable: :

        $ chmod +x MailHog

5.  Spin up another terminal window and start it there: :

        ./MailHog

6.  Check out <http://127.0.0.1:8025/> to see how it goes.

Now you have your own mail server running locally, ready to receive
whatever you send it.

### Sentry

Sentry is an error logging aggregator service. You can sign up for a
free account at <https://sentry.io/signup/?code=cookiecutter> or
download and host it yourself. The system is setup with reasonable
defaults, including 404 logging and integration with the WSGI
application.

You must set the DSN url in production.

Deployment
----------

The following details how to deploy this application.

### Heroku

See detailed [cookiecutter-django Heroku
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).
