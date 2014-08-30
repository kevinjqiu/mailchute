===============================
mailchute
===============================

|Build Status| |Coverage Status|


A mailinator-like service providing disposable email addresses

* Free software: BSD license
* Documentation: https://mailchute.readthedocs.org.

What is Mailchute
-----------------

Mailchute is an open source implementation of the [mailinator](http://mailinator.com) service intended for personal use. It consists of three components:

* smtpd - A simple SMTP server for receiving emails and store them
* api - A RESTful API for retrieving stored emails
* web - A web front-end for reading emails

.. |Build Status| image:: https://badge.fury.io/py/mailchute.png
    :target: http://badge.fury.io/py/mailchute

.. |Coverage Status| image:: https://coveralls.io/repos/kevinjqiu/mailchute/badge.png?branch=master
    :target: https://coveralls.io/r/kevinjqiu/mailchute?branch=master
