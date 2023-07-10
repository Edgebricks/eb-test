#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import os
import sys
import paramiko
import socket

from ebapi.common.logger import elog
from ebapi.common import utils as eutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RemoteMachine(object):
    """
    RemoteMachine API class implements::

        * connect - Connect to remote SSH server
        * run     - to run command on remote machine as specified user
        * get     - transfer file from remote machine to local machine
        * put     - transfer file from local machine to remote machine
        * close   - close all remote connections

    Examples:
        ::

            remote      = RemoteMachine(host, username, password)
            rc, output  = remote.run(cmd)
            assert rc  == 0
            match       = re.findall(pattern, output, re.M)
    """

    def __init__(
        self, host, username, port=22, timeout=20, password=None, keyfile=None
    ) -> None:
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host = host
        self.keyfile = keyfile
        self.username = username
        self.port = port
        self.password = password
        self.timeout = float(timeout)

    def connect(self):
        """
        Connect to the remote ssh server.

        Returns:
            bool: True on success or False on failure

        Args:
            hostname (string) : the server to connect to
            port (integer)    : the server port to connect to
            username (string) : the username to authenticate as (defaults to the current local username)
            password (string) : Used for password authentication; is also used for private key decryption if passphrase is not given.
            pkey (PKey)       : an optional private key to use for authentication
            timeout (float)   : an optional timeout (in seconds) for the TCP connect

        Examples:
            ::

                remote = RemoteMachine(host, username, password)
                remote.close
        """
        try:
            # Paramiko.SSHClient can be used to make connections to the remote
            # server and transfer files
            elog.info("Establishing ssh connection..")
            self.client = paramiko.SSHClient()
            # instructs the client to look for all the hosts connected to in the past by looking at the
            # system's known_hosts file and finding the SSH keys the host is
            # expecting
            self.client.load_system_host_keys()
            # Parsing an instance of the AutoAddPolicy to
            # set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Connect to the server
            if self.password == "":
                private_key = paramiko.RSAKey.from_private_key_file(self.keyfile)
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    pkey=private_key,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )
                elog.info("Connected to the server [%s]" % eutil.bcolor(self.host))
            else:
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )
                elog.info("Connected to the server [%s]" % eutil.bcolor(self.host))
        except paramiko.AuthenticationException:
            elog.error("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            elog.error(
                " Could not establish SSH connection: [%s]" % eutil.bcolor(sshException)
            )
            result_flag = False
        except socket.timeout as e:
            elog.error("Connection timed out" % eutil.bcolor(e))
            result_flag = False
        except Exception as e:
            elog.error("\nException in connecting to the server" % eutil.bcolor(e))
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        return result_flag

    def run(self, command):
        """
        Execute a command on the remote host.

        Returns:
            tuple: an integer status and a two strings,
                   the first containing stdout and
                   the second containing stderr from the command

        Args:
            command (string) : the command to execute

        Examples:
            ::

                remote = RemoteMachine(host, username, password)
                rc, output  = remote.run(command)
                assert rc  == 0
        """
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                elog.info("Executing command --> [%s]" % eutil.bcolor(command))
                stdout, stderr = self.client.exec_command(command, timeout=10)
                self.ssh_output = stdout.read()
                self.ssh_error = stderr.read()
                if self.ssh_error:
                    elog.error(
                        "Problem occurred while running command: [%s] - The error is %s"
                        % (eutil.bcolor(command), self.ssh_error)
                    )
                    result_flag = False
                else:
                    elog.info("Command execution completed successfully")
                self.client.close()
            else:
                elog.error("Could not establish SSH connection")
                result_flag = False
        except socket.timeout as e:
            elog.error("\nException in connecting to the server" % eutil.bcolor(e))
            self.client.close()
            result_flag = False
        except paramiko.SSHException:
            elog.error("Failed to execute the command: [%s]" % eutil.bcolor(command))
            self.client.close()
            result_flag = False

        return result_flag, self.ssh_output.strip()

    def get(self, remotePath, localPath):
        """
        download file/s from remote machine to local.

        Returns:
            bool: True on success or False on failure

        Args:
            remotePath (string): path to remote dir or file
            localPath  (string): destination path in local machine

        Examples:
            ::

                remote = RemoteMachine(host, username, password)
                assert remote.get('/tmp/download.txt', '/tmp')
        """
        result_flag = True
        try:
            if self.connect():
                download = self.client.open_sftp()
                download.get(remotePath, localPath)
                download.close()
                elog.info("[%s] download: success" % eutil.bcolor(self.host))
                self.client.close()
            else:
                elog.error("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            elog.error("[%s] download: failed" % eutil.bcolor(e))
            result_flag = False
            download.close()
            self.client.close()

        return result_flag

    def put(self, localPath, remotePath):
        """
        upload file/s from local machine to remote.

        Returns:
            bool: True on success or False on failure

        Args:
            localPath  (string): source path in local machine
            remotePath (string): destination path in remote

        Examples:
            ::

                remote = RemoteMachine(host, username, password)
                assert remote.put('/tmp/upload.txt', '/tmp', mode=755)
        """
        result_flag = True
        try:
            if self.connect():
                upload = self.client.open_sftp()
                upload.put(localPath, remotePath)
                upload.close()
                elog.info("[%s] put: success" % eutil.bcolor(self.host))
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            elog.error("[%s] put: failed" % eutil.bcolor(e))
            result_flag = False
            upload.close()
            self.client.close()

        return result_flag

    def close(self):
        """Close the SSH connection."""
        if self.connect():
            self.client.close()
