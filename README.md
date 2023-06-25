    © Copyright Edgebricks 2021

About eb-test
=============
eb-test is an automated test suite based on pytest framework to perform a full-fledged QA on Edgebricks Cloud with following features:
* Easy to deploy and run tests.
* Exactly takes 4 commands to deploy and run tests.
* Maintenance-free test framework. eb-test is based on [pytest](http://pytest.org/latest/>). pytest is a stable and well-maintained open-source test framework.
* Provides easy no-boilerplate testing. Helps developers, QA and support engineers to develop tests quickly with no-frills.
* Based on pytest, is easy to learn with rich documentation available online. Check out learning resources.
* Simple yet powerful!

API Automation
==============
Click [here](https://github.com/Edgebricks/eb-test/blob/master/ebapi/README.md) for details.

Execute below command to run all api tests::

    $ make run-api-tests

UI Automation
=============
Click [here](https://github.com/Edgebricks/eb-test/blob/master/ebui/README.md) for details.

Execute below command to run all api tests::

    $ make run-ui-tests

Documentation
=============
Click [here](https://github.com/Edgebricks/eb-test/blob/master/doc/README.md) for details.

Static Checks
=============
Install essential python static tools by running::

    $ sudo apt install -y flake8 black pylint autopep8 pycodestyle
    $ sudo apt install python3-pycodestyle python3-autopep8

This will install all required static check tools on the target machine.
Execute below command to run all staticchecks on the code::

    $ make staticchecks