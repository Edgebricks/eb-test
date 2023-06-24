#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import json
import requests

from ebapi.common.logger import elog


class RestClient(object):
    """
    RestClient API class, implements::

        * get
        * put
        * post
        * delete

    Examples:
        ::

            # first get token
            tokenObj = Token(scope='domain')
            token    = tokenObj.getToken()

            # create a RestClient object and make REST calls
            client   = RestClient(token)
            response = client.get(requestURL)
    """
    def __init__(self, token):
        self.token = token
        self.headers = {"Accept": "application/json",
                        "Content-Type": "application/json;charset=UTF-8",
                        "X-Auth-Token": self.token}

    def get(self, url, timeout=30):
        """
        implements GET rest api.

        Returns:
            a `response content <https://goo.gl/NeMqL8>`_

        Args:
            url (string): request URL.

            timeout(int): default 30 seconds.

        Examples:
            ::

                client   = RestClient(token)
                response = client.get(requestURL)
        """
        if not self.token:
            elog.error('token not found')
            return None

        elog.debug('URL = %s, Method = GET' % url)
        return requests.get(url=url, headers=self.headers, timeout=timeout)

    def put(self, url, payload={}, timeout=30):
        """
        implements PUT rest api.

        Returns:
            a `response content <https://goo.gl/NeMqL8>`_

        Args:
            url (string): request URL.

            payload(python dict): python dictonary in JSON format.

            timeout(int): default 30 seconds.

        Examples:
            ::

                client   = RestClient(token)
                payload  = {
                    'key1': value1,
                    'key2': value2
                }
                response = client.put(requestURL, payload)
        """
        if not self.token:
            elog.error('token not found')
            return None

        payload = json.dumps(payload)
        elog.debug('URL = %s, Method = PUT' % url)
        elog.debug('Payload = %s' % payload)
        return requests.put(url=url, headers=self.headers,
                            data=payload, timeout=timeout)

    def post(self, url, payload={}, timeout=30):
        """
        implements POST rest api.

        Returns:
            a `response content <https://goo.gl/NeMqL8>`_

        Args:
            url (string): request URL.

            payload(python dict): python dictonary in JSON format.

            timeout(int): default 30 seconds.

        Examples:
            ::

                client   = RestClient(token)
                payload  = {
                    'key1': value1,
                    'key2': value2
                }
                response = client.post(requestURL, payload)
        """
        if not self.token:
            elog.error('token not found')
            return None

        payload = json.dumps(payload)
        elog.debug('URL = %s, Method = POST' % url)
        elog.debug('Payload = %s' % payload)
        return requests.post(url=url, headers=self.headers,
                             data=payload, timeout=timeout)

    def patch(self, url, payload={}, timeout=30):
        """
        implements PATCH rest api.

        Returns:
            a `response content <https://goo.gl/NeMqL8>`_

        Args:
            url (string): request URL.

            payload(python dict): python dictonary in JSON format.

            timeout(int): default 30 seconds.

        Examples:
            ::

                client   = RestClient(token)
                payload  = {
                    'key1': value1,
                    'key2': value2
                }
                response = client.patch(requestURL, payload)
        """
        if not self.token:
            elog.error('token not found')
            return None

        payload = json.dumps(payload)
        elog.debug('URL = %s, Method = PATCH' % url)
        elog.debug('Payload = %s' % payload)
        return requests.patch(url=url, headers=self.headers,
                             data=payload, timeout=timeout)

    def delete(self, url, timeout=30):
        """
        implements DELETE rest api.

        Returns:
            a `response content <https://goo.gl/NeMqL8>`_

        Args:
            url (string): request URL.

            timeout(int): default 30 seconds.

        Examples:
            ::

                client   = RestClient(token)
                response = client.delete(requestURL)
        """
        if not self.token:
            elog.error('token not found')
            return None

        elog.debug('URL = %s, Method = DELETE' % url)
        return requests.delete(url=url, headers=self.headers,
                              timeout=timeout)

    def deleteWithPayload(self, url, payload={}, timeout=30):
        """
        implements DELETE rest api.

        Returns:
            a `response content <https://goo.gl/NeMqL8>`_

        Args:
            url (string): request URL.

            timeout(int): default 30 seconds.

        Examples:
            ::

                client   = RestClient(token)
                response = client.delete(requestURL)
        """
        if not self.token:
            elog.error('token not found')
            return None

        payload = json.dumps(payload)
        elog.debug('URL = %s, Method = DELETE' % url)
        return requests.delete(url=url, headers=self.headers,
                              data=payload, timeout=timeout)

