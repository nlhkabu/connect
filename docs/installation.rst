Installation
============

Connect is currently tested with ``Python 3.4`` and ``Django 1.7 & 1.8``.


Dependencies
____________

Assuming you have the following installed:

* Python 3
* pip
* virtualenv-wrapper
* PostgreSQL (although sqlite can be used on dev machines)

You may also need to install `libyaml`:

.. code-block:: bash

    # On Ubuntu
    $ sudo apt-get install libyaml-dev

    # Or Fedora
    $ sudo yum install libyaml-devel


Next setup your virtualenv with:

.. code-block:: bash

    $ mkvirtualenv --python=/usr/bin/python3 connect
    $ pip install -r requirements/dev.txt


Postgres setup
______________

Postgres is not required for local development, but it can be a good idea --
running tests against the same database as production can sometimes pick up
edge case bugs early.

If you're setting up a staging, production, or CI server, postgres is strongly
recommended. Install it with `sudo apt-get install postgresql-9.4` or similar,
and then set up a database for the connect app:

.. code-block:: bash

    $ createdb connectdb
    $ createuser -P connectuser   # note password chosen
    $ psql

    =# GRANT ALL PRIVILEGES ON DATABASE connectdb TO connectuser;
    =# ALTER USER connectuser CREATEDB;

    =# \l # Check database access permissions
    =# \q # (or Ctrl-D) Exit from psql

(You can substitute *connectdb* and *connectuser* as you wish, you will just need to reflect that in the `DATABASE_URL` you set below.)


Environment variables
_____________________

A fully configured connect instance requires the following environment variables:

* `DATABASE_URL` -- db config syntax: "postgres://USER:PASSWORD@HOST:PORT/DB-NAME"
* `SECRET_KEY` -- this should not be stored in your repository.
* `ALLOWED_HOSTS` -- required when DEBUG=False, so for staging/ci/prod.
* `DEFAULT_FROM_EMAIL` -- the from address for in-app emails
* `MANDRILL_API_KEY` -- Mandrill is recommend for sending emails from the server
* `DJANGO_MODE` -- outside dev, set this to "Production" or "Staging"

All of these have working defaults in dev, but if you want to override any of
them (eg to use postgres), you can set them like this:


.. code-block:: bash

    export DATABASE_URL="postgres://connectuser:<password>@localhost:5432/connectdb"
    export SECRET_KEY="<a long string of random characters"
    export DEFAULT_FROM_EMAIL="admin@mentorconnect.com"
    #... etc

**TIP:** a good place to set them is in the ``postactivate`` virtualenv hook,
which will be somewhere like *~/.virtualenvs/connect/bin/postactivate*. For
neatness, unset them in the ``predeactivate`` virtualenv hook too:

.. code-block:: bash

    unset DATABASE_URL
    unset SECRET_KEY
    unset DEFAULT_FROM_EMAIL
    #... etc


Additional configuration
________________________


In ``settings.py``, you may also wish to override:

    * Admins
    * Timezone
    * Gravatar Settings



Initial database setup
_______________________

First sync the database:

.. code-block:: bash

    $ python manage.py migrate


Then create a superuser:

.. code-block:: bash

    $ python manage.py createsuperuser


Now you can run your local sever:

.. code-block:: bash

    $ python manage.py runserver

And you'll be able to open up the development site in your web browser at http://localhost:8000/


.. important::
    Now that your site is up and running, you will need to login to the admin and:

    #. Set ``is_moderator`` to ``True`` for your superuser.
    #. Set up some additional data in your database. (See :doc:`configuration` for more information.)


Edit scss files (style)
_______________________

Connect is built with Sass_ and Compass_.

If you need to install them, you will also need ``ruby`` but the installation process is beyond the scope of this project.

Please refer to the Saas and Compass documentation.


To compile locally your scss changes to the css file, use the command ``compass compile`` in the ``static/css`` folder of the app concerned by the changes.


.. _Sass: http://sass-lang.com/
.. _Compass: http://compass-style.org/


.. rubric:: Example: Changing the highlighting color

You can change the default pink highlight color by editing the ``$highlight``
variable at the top of ``static/css/sass/_color.scss``


Running Tests
_____________

.. code-block:: bash

    $ ./manage.py test #to test the entire project.
    $ ./manage.py test <appname> #to test a specific django app


To run Connect's `Behave`_ tests, you will need to have PhantomJS_ installed.

.. code-block:: bash

    $ npm install phantomjs


Run the BDD tests with:

.. code-block:: bash

    $ ./manage.py test bdd

To run an individual test feature, use

.. code-block:: bash

    $ npm install phantomjs
    $ ./manage.py test bdd --behave_include featurename


Alternatively you can use any other `supported browser`_ (e.g. Chrome, Firefox)
by installing it on your system and specifying it when you run your tests:

.. code-block:: bash

    $ ./manage.py test bdd --behave_browser <browser>

.. _Behave: http://pythonhosted.org/behave/
.. _PhantomJS: http://phantomjs.org/
.. _`supported browser`: http://splinter.cobrateam.info/en/latest/index.html#drivers

