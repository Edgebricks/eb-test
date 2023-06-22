#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


"""ebtest library with network utility functions"""
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


class CinderBase(Token):
    def __init__(self, projectID, scope='project'):
        super(CinderBase, self).__init__(scope)
        self.client     = RestClient(self.getToken())
        self.projectID  = projectID
        self.serviceURL = self.getServiceURL()
        self.cinderURL  = self.serviceURL + '/cinder/v2/' + self.projectID


class Volumes(CinderBase):
    """
    class that implements CRUD opertation for Volume/Block Storage
    """
    def __init__(self, projectID):
        super(Volumes, self).__init__(projectID)
        self.volumesURL  = self.cinderURL + '/volumes'

    def deleteVolume(self, volumeID):
        """
        Returns:
            `response content <https://goo.gl/NeMqL8>`_ after deleting volume.

        Args:
            volumeID (string): voulme ID to be deleted.

        Examples:
            ::

                volumeObj = Volumes(projectID)
                response  = volumeObj.deleteVolume(volumeID)
        """
        requestURL = self.volumesURL + '/' + volumeID
        return self.client.delete(requestURL)
