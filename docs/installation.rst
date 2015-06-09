Installation
============

Connect is currently tested with ``Python 3.3`` and ``Django 1.7``.


Dependencies
____________

Assuming you have the following installed:

* python 3
* pip
* virtualenv-wrapper
* PostgreSQL (although sqlite can be used on dev machines)

You will also need to install a YAML parser:

.. code-block:: bash

    # On Ubuntu
    $ sudo apt-get install libyaml-dev

    # Or Fedora
    $ sudo yum install libyaml-devel


Next setup your virtualenv with:

.. code-block:: bash

    $ mkvirtualenv --python=/usr/bin/python3 <appname>
    $ pip install -r requirements/dev.txt


Creating your database
_________________________

Using PostgreSQL:

.. code-block:: bash

    $ createdb <appname>
    $ createuser -P <appname>
    $ psql

    $ GRANT ALL PRIVILEGES ON DATABASE <appname> TO <appname>;
    $ ALTER USER <appname> CREATEDB;

    $ \l # Check database access permissions
    $ \q # (or Ctrl-D) Exit from psql

If you've decided to use sqlite in dev, then you don't need to run anything at
this point.

Configuring your environment
____________________________

In your ``postactivate`` virtualenv hook, set the following environment variables:

.. code-block:: bash

    export SECRET_KEY="<a long random string>"  # optional in dev
    export DATABASE_URL="postgres://<appname>:<password>@localhost:5432/<appname>"
    export DEFAULT_FROM_EMAIL="<email you want to send in-app emails from>"

In you ``predeactivate`` virtualenv hook:

.. code-block:: bash

    unset SECRET_KEY
    unset DATABASE_URL
    unset DEFAULT_FROM_EMAIL

If you want to use sqlite (not recommended for staging, CI or production), then
set DATABASE_URL to something like this:

.. code-block:: bash

    export DATABASE_URL="sqlite:///home/yourusername/path/to/db.sqlite"


In ``settings.py``, you may also wish to override:

    * Admins
    * Timezone
    * Gravatar Settings


Setting up the Database
_______________________

.. note::
    To use the ``./`` shortcut you will need to change your ``manage.py``
    permissions to ``rwxrw-r--``.

First sync the database:

.. code-block:: bash

    $ ./manage.py migrate


Then create a superuser:

.. code-block:: bash

    $ ./manage.py createsuperuser


Now you can run your local sever:

.. code-block:: bash

    $ ./manage.py runserver


.. important::
    Now that your site is up and running, you will need to login to the admin and:

    #. Set ``is_moderator`` to ``True`` for your superuser.
    #. Set up some additional data in your database. (See :doc:`configuration` for more information.)


Changing the Color
__________________

Connect is built with Sass_.

You can change the default pink highlight color by editing the ``$highlight``
variable at the top of ``static/css/sass/_color.scss``

.. _Sass: http://sass-lang.com/


Running Tests
_____________

.. code-block:: bash

    $ ./manage.py test #to test the entire project.
    $ ./manage.py test <appname> #to test a specific app


To run Connect's `Behave`_ tests, you will need to have PhantomJS_ installed.

.. code-block:: bash

    $ npm install phantomjs
    $ ./manage.py test bdd

To run an individual test, use

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

