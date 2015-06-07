=======
Connect
=======

Connect is a moderated web application that helps members connect with
each other based on skills, interests and location.

Connect is in active development and is not yet feature complete.
Please see ``TODO.rst`` for major planned features.

.. image:: https://travis-ci.org/nlhkabu/connect.svg?branch=master
    :target: https://travis-ci.org/nlhkabu/connect


Documentation
_____________

Documentation is available at http://django-mentor-connect.readthedocs.org/en/latest/

.. image:: https://readthedocs.org/projects/django-mentor-connect/badge/?version=latest
    :target: https://readthedocs.org/projects/django-mentor-connect/?badge=latest
    :alt: Documentation Status


Demo
____

A demo version of Connect is available to try at http://kabu-connect.herokuapp.com

Use the following authentication details to login:

| **Standard User:**
| email: standard@test.test
| password: demo
|
| **Moderator:**
| email: moderator@test.test
| password: demo
|



Contributing
____________

After cloning the repo, install the requirements with:

    pip install -r requirements/dev.txt

Create a local admin account with

    python manage.py createsuperuser

And then check out the site with

    python manage.py runserver


If you want to contribute changes to the code, you'll want to run the test suite.

Run the unit tests with

    python manage.py test

And run the BDD tests with

    python manage.py test bdd

To run an individual BDD feature, use, eg:

    python manage.py test bdd --behave_include logout

If you don't want to install and configure postgres on your laptop, you can
override the default database using the DATABASE_URL environment variable, eg:

    export DATABASE_URL=sqlite:///`pwd`/db.sqlite


Make sure all the BDD tests pass before submitting any PRs, and feel free to
add yourself to AUTHORS.rst if you want the glory!



Licence
_______

Connect is BSD licenced.

If you are using Connect for your group or organisation, we'd love to know about it.
Please add yourself to ``USERS.rst``
