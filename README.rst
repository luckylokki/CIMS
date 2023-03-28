###############################################################################
                            COMPUTER INVENTORY MANAGEMENT SYSTEM
###############################################################################

This is a project for inventory devices in office.
This is done using the `Django`_ framework.

.. _Python training course: https://github.com/shorodilov/python-course.git
.. _Flask: https://docs.djangoproject.com/en/4.1/

Getting started
===============

#. Download the code base
#. Install the dependencies
#. Run the project

Preparing manual run
===============

To install the requirements use one of the commands below:

.. code-block::

    pip install -r requirements.txt

Make migrations:


.. code-block::

    python manage.py makemigrations inventory
    python manage.py makemigrations staff
    python manage.py migrate

Run server
=====================
Normal run:

.. code-block::

    python manage.py runserver

DEBUG mode run:

.. code-block::

    python DJANGO_DEBUG=1 manage.py runserver

You can find DB user,password and host from docker-compose.yaml

Docker-compose use
===============
Normal run:

.. code-block::

    docker-compose up -d

DEBUG mode run:

.. code-block::

    docker-compose -f docker-compose-dev.yaml up -d