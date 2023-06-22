    © Copyright Edgebricks 2021

UI Automation
=============

Requirements
============
python-pip package should be available on the target machine.

If not, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Install it by running::

    $ sudo apt install -y python3-pip python3-virtualenv

This will install pip on the target machine.

Deploy
======
Basic steps::

    1. git clone git@github.com:Edgebricks/eb-test.git -b master
    2. cd eb-test
    3. cd ebui
    4. python3 -m pip install -r requirements.txt
    5. export PYTHONDONTWRITEBYTECODE=1

To deploy eb-test in an isolated/virtual environment without conflicts with existing envrionment::

    1. pip install virtualenv
    2. git clone git@github.com:Edgebricks/eb-test.git -b master
    3. cd eb-test
    4. cd ebui
    5. virtualenv venv
    6. source venv/bin/activate
    7. python3 -m pip install -r requirements.txt
    8. export PYTHONDONTWRITEBYTECODE=1

After running tests, to deactivate the virtual environment, run the following comand in venv::

    (venv):~$ deactivate

**NOTE**: If setup fails to install python cryptography module, ensure that libssl-dev libffi-dev python-dev libraries are installed on the system.

Running Tests
=============
`TO BE ADDED`

Test Results
============
`TO BE ADDED`
