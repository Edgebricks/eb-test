About eb-test
============

eb-test is an automated test suite based on pytest framework to perform a full-fledged QA on Edgebricks Cloud::

    © Copyright Edgebricks 2021

eb-test has following advantages

* easy to deploy and run tests. Exactly takes 4 commands to deploy and run tests.
* maintenance-free test framework. eb-test is based on [pytest](http://pytest.org/latest/>). pytest is a stable and well-maintained open-source test framework.
* provides easy no-boilerplate testing. Helps developers, QA and support engineers to develop tests quickly with no-frills.
* eb-test, based on pytest, is easy to learn with rich documentation available online. Check out learning resources.
* simple yet powerful!

Install
=======

Requirements
============

python-pip package should be available on the target machine.

If not, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Install it by running::

    $ sudo apt install -y python3-pip

This will install pip on the target machine.

Deploy
======

Basic steps::

    1. git clone git@github.com:Edgebricks/eb-test.git -b master
    2. cd eb-test
    3. python3 -m pip install -r requirements.txt
    4. export PYTHONDONTWRITEBYTECODE=1

To deploy eb-test in an isolated/virtual environment without conflicts with existing envrionment::

    1. pip install virtualenv
    2. git clone git@github.com:Edgebricks/eb-test.git -b master
    3. cd eb-test
    4. virtualenv venv
    5. source venv/bin/activate
    6. python3 -m pip install -r requirements.txt
    7. export PYTHONDONTWRITEBYTECODE=1

After running tests, to deactivate the virtual environment, run the following comand in venv::

    (venv):~$ deactivate

**NOTE**: If setup fails to install python cryptography module, ensure that libssl-dev libffi-dev python-dev libraries are installed on the system.

Running Tests
=============

Run tests from eb-test directory::

    python3 -m pytest --html=<file-name.html> <options> <path_to_test_dir_or_file>

| command | description |
| ------- | ----------- |
| python3 -m pytest tests | To run all tests |
| python3 -m pytest --html=result.html suites | To save test run in result.html |
| python3 -m pytest -s tests | To see entire test result in console |

The --html option will save the test output in specified path in an html file.
If this option is omitted then the test result will be stored as test-result.html.

Test Results
============

Test results are available in 2 formats::

    1. html log (Default, test-result.html from the execution diretory)
        OR
    2. console log

console log can be obtained by using option '-s' with py.test::

    python3 -m pytest -s <option>
