#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import pytest

from ebtest.common.config import ConfigParser
from ebtest.common.commands import RemoteMachine

testConfig = ConfigParser('remote')
host       = testConfig.getConfig('host')
userName   = testConfig.getConfig('username')
password   = testConfig.getConfig('password')
port       = testConfig.getConfig('port')

@pytest.fixture()
def test_remoteVMIsLinux(request):
    remote = RemoteMachine(host, userName, password, port)

    def cleanup():
        remote.close()
    request.addfinalizer(cleanup)

    status, output = remote.run('uname -a')
    assert status == 0
    assert 'Linux' in output
    remote.close()


@pytest.fixture()
def test_ethSpeed(request):
    remote = RemoteMachine(host, userName, password, port)

    def cleanup():
        remote.close()
    request.addfinalizer(cleanup)

    status, output = remote.run('sudo ethtool eno1 | grep Speed | cut -d : -f2')
    assert status == 0
    assert '10000Mb/s' in output
    remote.close()


@pytest.fixture()
def test_invalidCommand(request):
    remote = RemoteMachine(host, userName, password, port)

    def cleanup():
        remote.close()
    request.addfinalizer(cleanup)

    status, output = remote.run('crap command')
    assert status != 0
    status, output = remote.run('ls -l')
    assert status == 0
    assert output
    remote.close()


@pytest.fixture()
def test_download(request):
    remote = RemoteMachine(host, userName, password, port)

    def cleanup():
        remote.close()
    request.addfinalizer(cleanup)

    cmd = "echo 'transferring contents to mac' > /tmp/download.txt"
    status, _ = remote.run(cmd)
    assert status == 0
    status = remote.get('/tmp/download.txt', '/tmp')
    assert status
    remote.close()

@pytest.fixture()
def test_upload(request):
    remote = RemoteMachine(host, userName, password, port)

    def cleanup():
        remote.close()
    request.addfinalizer(cleanup)

    status = remote.put('/tmp/upload.txt', '/tmp', mode=755)
    assert status
    remote.close()
