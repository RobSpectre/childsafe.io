*************
Garfield
*************

A communications platform for deterring high frequency buyers of underground
commercial sex.

Powered by `Django`_ and `Twilio`_.


.. image:: https://travis-ci.org/RobSpectre/garfield.svg?branch=master
    :target: https://travis-ci.org/RobSpectre/garfield

.. image:: https://codecov.io/gh/RobSpectre/garfield/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/RobSpectre/garfield


**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none


Installation
===========

Install this `Django`_ application by first cloning the repository.

.. code-block:: bash
  
    git clone https://github.com/RobSpectre/garfield


Install the Python dependencies.

.. code-block:: bash

    cd garfield
    pip install -r requirements.txt


Create a local configuration file and customize with your settings.

.. code-block:: bash
   
    cd garfield/garfield/garfield
    cp local.sample local.py


Create database.

.. code-block:: bash

    cd ..
    python manage.py makemigrations
    python manage.py migrate

Run the server

.. code-block:: bash

    python manage.py runserver

Configure a `Twilio phone number`_ to point to the `/sms` endpoint of your host.

.. image:: https://raw.githubusercontent.com/RobSpectre/garfield/master/garfield/garfield/static/images/twilio_phone_number_screenshot.png 
    :target: https://www.twilio.com/console/phone-numbers/incoming

Text "HELP" to the number you configured.


Development
===========

Hacking
-----------

Install `RabbitMQ`_, required for the Celery task queue. Instructions for
Ubuntu.

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install rabbitmq-server


To hack on the project, fork the repo and then clone locally.

.. code-block:: bash

    $ git clone https://github.com/RobSpectre/garfield.git

Move to the project directory.

.. code-block:: bash

    $ cd garfield 

Install the Python dependencies (preferably in a virtualenv).

.. code-block:: bash

    $ pip install -r requirements.txt 

Then customize your local variables to configure your `Twilio`_, email and
admin accounts you want to receive tips.

.. code-block:: bash

    $ cp garfield/garfield/local.sample garfield/garfield/local.py
    $ vim garfield/garfield/local.py

Move to the Django project root.

.. code-block:: bash

    $ cd garfield

Start the Celery task queue.


.. code-block:: bash

    $ celery -A garfield worker -l info 


Start the Django app.

.. code-block:: bash

    $ python manage.py runserver 


Testing
------------

Use Tox for easily running the test suite.

.. code-block:: bash

    $ tox


Meta
============

* Written by `Rob Spectre`_
* Released under `MIT License`_
* Software is as is - no warranty expressed or implied.


.. _Rob Spectre: http://www.brooklynhacker.com
.. _MIT License: http://opensource.org/licenses/MIT
.. _Django: https://www.djangoproject.com/
.. _Twilio: https://twilio.com
.. _Twilio phone number: https://www.twilio.com/console/phone-numbers/incoming
.. _RabbitMQ: https://www.rabbitmq.com/download.html
