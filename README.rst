===============================
mailchute
===============================

.. image:: https://badge.fury.io/py/mailchute.png
    :target: http://badge.fury.io/py/mailchute

.. image:: https://travis-ci.org/kevinjqiu/mailchute.png?branch=master
        :target: https://travis-ci.org/kevinjqiu/mailchute

.. image:: https://pypip.in/d/mailchute/badge.png
        :target: https://pypi.python.org/pypi/mailchute


A mailinator-like service providing disposable email addresses

* Free software: BSD license
* Documentation: https://mailchute.readthedocs.org.

What is Mailchute
-----------------

Mailchute is an open source implementation of the [mailinator](http://mailinator.com) service intended for personal use. It consists of three components:

* smtpd - A simple SMTP server for receiving emails and store them
* api - A RESTful API for retrieving stored emails
* web - A web front-end for reading emails

