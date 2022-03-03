.. install:

=======
Install
=======

Requirements
============

*python-pip* package **should be** availble on the target machine.

If not, install it by running::

    $ sudo apt install -y python3-pip

This will install pip on the target machine.

Deploy
======


Follow either Basic Deployment or Isolated Deployment.

Basic Deployment::

    1. git clone git@github.com:Edgebricks/eb-test.git
    2. cd eb-test
    3.  python3 -m pip install -r requirements.txt
    4. export PYTHONDONTWRITEBYTECODE=1

To deploy zstest in an isolated/virtual environment without conflicts with existing envrionment.

Isolated Deployment::

    1. pip install virtualenv
    2. git clone ssh://<userName>@code.corp.zerostack.net:29418/zstest
    3. cd zstest
    4. virtualenv venv
    5. source venv/bin/activate
    6.  python3 -m pip install -r requirements.txt
    7. export PYTHONDONTWRITEBYTECODE=1


After running tests, to deactivate the virtual environment, run the following command in venv::

    (venv):~$ deactivate
