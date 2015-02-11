Installation
============

Connect is currently tested with ``Python 3.3`` and ``Django 1.7``.


Dependencies
____________

Assuming you have the following installed:

* python 3
* pip
* PostgreSQL
* virtualenv-wrapper

You will also need to install a YAML parser:

.. code-block:: bash

    # On Ubuntu
    $ sudo apt-get install libyaml-dev

    # Or Fedora
    $ sudo yum install libyaml-devel


Next setup your environment with:

.. code-block:: bash

    $ mkvirtualenv --python=/bin/python3 connect
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


Settings.py
___________

The following settings should be configured:


.. ~todo
    * secret key
    * admins
    * database settings
    * timezone
    * language
    * gravatar settings
    * site settings
    * email settings


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


Then you can run your local sever:

.. code-block:: bash

    $ ./manage.py runserver


.. important::
    Now that your site is up and running, you will need to:

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


To run Connect's behavioural tests, you will need to have PhantomJS_ installed.

Alternatively you can use any other `supported browser`_ (e.g. Chrome, Firefox)
by installing it on your system and specifying it when you run your tests:

.. code-block:: bash

    $ ./manage.py test <appname> --behave_browser <browser>

.. _PhantomJS: http://phantomjs.org/
.. _`supported browser`: http://splinter.cobrateam.info/en/latest/index.html#drivers
