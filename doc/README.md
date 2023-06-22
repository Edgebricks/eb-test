    © Copyright Edgebricks 2021

Documentation
=============
Requirements
============
python-pip package should be available on the target machine.

If not, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Install it by running::

    $ sudo apt install -y python3-pip python3-dev python3-setuptools apache2 -y
    $ pip3 install --upgrade pip
    $ sudo apt-get install python3-sphinx sphinx-common libjs-sphinxdoc=1.8.5-7ubuntu3 sphinx_rtd_theme rst2pdf

This will install pip and related packages on the target machine.

Build API documentation
=======================
Run tests from doc directory::

    $ make clean && make html

Build UI documentation
======================
`TO BE ADDED`