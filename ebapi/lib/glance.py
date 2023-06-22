#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


"""ebtest library with network utility functions"""
import json

from ebapi.common import utils as eutil
from ebapi.common import logger as elog
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


class GlanceBase(Token):
    def __init__(self, projectID, scope='project'):
        super(GlanceBase, self).__init__(scope)
        self.client     = RestClient(self.getToken())
        self.projectID  = projectID
        self.serviceURL = self.getServiceURL()
        self.glanceURL  = self.serviceURL + '/glance/v2'


class Images(GlanceBase):
    """
    class that implements CRUD operation for Images
    """
    def __init__(self, projectID):
        super(Images, self).__init__(projectID)
        self.imagesURL  = self.glanceURL + '/images'

    def createCirrosImageByURL(self, imageName='', netID=''):
        """
        Returns:
            response imageID <https://goo.gl/NeMqL8>`_ after creating Image.

        Args:
            imageName (string): Name of the image to be created.
            domainID  (uuid)  : Domain ID.

        Examples:
            ::

                imageObj = Images(projectID)
                response  = imageObj.createCirrosImageByURL(imageName, domainID)
        """
        requestURL = self.glanceURL + '/tasks'
        payload = {
            "type": "import",
            "input": {
                "import_from": "http://download.cirros-cloud.net/0.5.2/cirros-0.5.2-x86_64-disk.img",
                "import_from_format": "qcow2",
                "image_properties": {
                    "name": imageName,
                    "disk_format": "qcow2",
                    "min_ram": 2048,
                    "os": "Cirros",
                    "version": "0.5.2",
                    "source": "url",
                    "category": "url",
                    "imageAccess": "currentProject",
                    "owner": self.projectID,
                    "created_version": "v2",
                    "hw_vif_multiqueue_enabled": "true",
                    "buAccess": "",
                    "visibility": "private",
                    "changeDefaultConfig": "true",
                    "min_disk": 1,
                    "volume-type": "relhighiops_type",
                    "import_from": "http://download.cirros-cloud.net/0.5.2/cirros-0.5.2-x86_64-disk.img",
                    "container_format": "ovf",
                    "net_id": netID
                }
            }
        }
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('failed to create image: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return False

        elog.logging.info('image %s created successfully: %s'
                  % (eutil.bcolor(imageName),
                     eutil.bcolor(response.status_code)))
        return True

    def deleteImage(self, imageID):
        """
        Returns:
            `response content <https://goo.gl/NeMqL8>`_ after deleting volume.

        Args:
            imageID (string): Image ID to be deleted.

        Examples:
            ::

                ImageObj = Images(projectID)
                response  = ImageObj.deleteImage(imageID)
        """
        requestURL = self.imagesURL + '/' + imageID
        response = self.client.delete(requestURL)
        if not response.ok:
            elog.logging.error('failed to delete image: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return False

        elog.logging.info('deleting image %s: %s OK'
                  % (eutil.bcolor(imageID),
                     eutil.gcolor(response.status_code)))
        return True

    def getImagesbyVisibility(self, visibility):
        """
        Returns:
            `response content <https://goo.gl/NeMqL8>`_ after getting image.

        Args:
            visibility (string): visibility.

        Examples:
            ::

                ImageObj = Images(projectID)
                response  = ImageObj.getImagesbyVisibility(visibility)
        """
        requestURL = self.imagesURL + '?visibility=%s' % visibility
        response   = self.client.get(requestURL)
        return json.loads(response.content)

    def getImagesbyOwner(self, owner):
        """
        Returns:
            `response content <https://goo.gl/NeMqL8>`_ after getting image.

        Args:
            owner (string): owner.

        Examples:
            ::

                ImageObj = Images(projectID)
                response  = ImageObj.getImagesbyOwner(owner)
        """
        requestURL = self.imagesURL + '?owner=%s' % owner
        response   = self.client.get(requestURL)
        return json.loads(response.content)
