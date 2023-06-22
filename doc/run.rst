.. run:

==========
Test Setup
==========

Set the test configuration values in test configuration file located at::

    ebtest/test.conf

The test configuration values can obtained from an existing cloud using `inspect <https://developers.google.com/web/tools/chrome-devtools>`_ call or from ecli.

Example::

    [configs]
    apiurl = https://console.staging.edgebricks.com
    acctid = b10e48c7-54a1-493e-9ef1-231af924f1c6
    clusterid = cb7fb189-f0b9-41cc-8622-d9c00e2efb1c
    projectid = 0d262dfb843b4757958a7f16d680fcb8
    setupname = Dev10
    domainid = 42a3c79004c4415bb09444cb2ea3afff
    domainname = testdomain
    cloudadmin = admin
    cloudadminpassword = test123
    projectname = testproject
    projectadmin = tenant
    projectadminpassword = tenantpassword
    projectmember = test
    projectmemberpassword = test123


=============
Running Tests
=============

Run tests from eb-test/ebtest directory ::

    pytest --html=<file-name.html> <options> <path_to_test_dir_or_file>

Example:

    ===  ==================================== ==============================
    #       command                            description
    ===  ==================================== ==============================
    1      pytest ebtest/tests                 To run all tests
    4      pytest ebtest/tests/networking      To run all networking tests
    6      pytest --html=result.html suites    To save test run in result.html
    7      pytest -s ebtest/tests              To see entire test result in console
    ===  ==================================== ==============================

The --html option will save the test output in specified path in an html file. If this option is omitted then the test result is saved as test-result.html in CWD.
