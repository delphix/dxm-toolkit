#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2018 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : March 2018
# Comments: List of the Database connectors


import logging
from dxm.lib.DxConnector.DxConnector import DxConnector
from masking_apis.apis.file_connector_api import FileConnectorApi
from masking_apis.models.file_connector import FileConnector
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxFileConnector(DxConnector, FileConnector):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DxConnector.__init__(self, engine)
        FileConnector.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating FileConnector object")

    @property
    def connectorId(self):
        return self.file_connector_id

    @property
    def host(self):
        return self.connection_info.host

    @property
    def port(self):
        return self.connection_info.port

    def get_type_properties(self):
        """
        Return dict with properties specific for connector type
        """
        props = {
            'login_name': self.connection_info.login_name,
            'path': self.connection_info.path,
            'connection_mode': self.connection_info.connection_mode
        }
        return props

    def get_properties(self):
        """
        Return dict with properties required for connector type
        """

        props = {
            'host': self.connection_info.host,
            'username': self.connection_info.login_name,
            'connectorName': self.connector_name,
            'password': self.connection_info.password,
            'fileType': self.file_type,
            'environmentId': self.environment_id,
        }

        empty = 0
        for k in props.keys():
            if (props[k] is None):
                print "Property %s can't be empty" % k
                empty = empty + 1

        if empty == 0:
            return props
        else:
            return None

    def add(self):
        """
        Add connector to engine
        Return None if OK
        """
        payload_dict = self.get_properties()
        if payload_dict is None:
            print_error('Some required property not found')
            return 1

        try:
            self.__logger.debug("create connector input %s" % str(self))

            api_instance = FileConnectorApi(self.__engine.api_client)
            response = api_instance.create_file_connector(
                self,
                _request_timeout=self.__engine.get_timeout())
            self.file_connector_id = response.file_connector_id

            self.__logger.debug("connector response %s"
                                % str(response))

            print_message("Connector %s added" % self.connector_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete connector from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = FileConnectorApi(self.__engine.api_client)

        try:
            self.__logger.debug("delete connector id %s"
                                % self.environment_id)
            response = api_instance.delete_file_connector(
                self.file_connector_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("delete connector response %s"
                                % str(response))
            print_message("Connector %s deleted" % self.connector_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def test(self):
        """
        Test connector connection to database
        Return None if OK
        """

        api_instance = FileConnectorApi(self.__engine.api_client)

        try:
            self.__logger.debug("test connector id %s"
                                % self.environment_id)
            response = api_instance.test_file_connector(
                self.file_connector_id,
                _request_timeout=self.__engine.get_timeout())
            if response.response == "Connection Failed":
                print_error("Connector test %s failed" % self.connector_name)
                return 1
            else:
                print_message("Connector test %s succeeded"
                              % self.connector_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def fetch_meta(self):
        """
        Fetch list of tables
        Return list if OK
        None if no objects
        """

        api_instance = FileConnectorApi(self.__engine.api_client)

        try:
            self.__logger.debug("fetch connector id %s"
                                % self.environment_id)
            response = api_instance.fetch_file_metadata(
                self.file_connector_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("list of tables" + str(response))
            return response
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return None
