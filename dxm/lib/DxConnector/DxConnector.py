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
from masking_apis.models.database_connector import DatabaseConnector
from masking_apis.apis.database_connector_api import DatabaseConnectorApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxConnector(DatabaseConnector):

    @property
    def connector_type(self):
        """
        connector_type
        """
        if self.is_database:
            return self.database_type
        else:
            return self.file_type

    @property
    def is_database(self):
        """
        return not None if this is a database connectors
        """
        return self.__is_database

    @is_database.setter
    def is_database(self, is_database):
        """
        set value if this is a database connectors
        """
        self.__is_database = is_database

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DatabaseConnector.__init__(self)
        self.__is_database = None
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxConnector object")

    def from_connector(self, con):
        """
        Copy properties from DatabaseConnector object into DxConnector
        :param con: DatabaseConnector object
        """
        self.__dict__.update(con.__dict__)

    def get_properties(self):
        """
        get_properties is abstract method - implement in vendor class
        """
        raise NotImplementedError("Please Implement this method")

    def add(self):
        """
        Add connector to engine
        Return 0 if OK
        """
        payload_dict = self.get_properties()
        if payload_dict is None:
            print_error('Some required property not found')
            return 1

        try:
            self.__logger.debug("create connector input %s" % str(self))
            api_instance = DatabaseConnectorApi(self.__engine.api_client)
            response = api_instance.create_database_connector(
                self,
                _request_timeout=self.__engine.get_timeout())
            self.database_connector_id = response.database_connector_id

            self.__logger.debug("connector response %s"
                                % str(response))

            print_message("Connector %s added" % self.connector_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    def update(self):
        """
        Update connector on engine
        Return None if OK
        """

        api_instance = DatabaseConnectorApi(self.__engine.api_client)
        body = DatabaseConnector()

        del body.password

        for k in self.attribute_map.keys():
            if getattr(self, k) is not None:
                setattr(body, k, getattr(self, k))

        print body

        try:
            self.__logger.debug("update connector input %s" % str(self))
            response = api_instance.update_database_connector(
                self.database_connector_id,
                body,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("update connector response %s"
                                % str(response))

            self.database_connector_id = response.database_connector_id
            print_message("Connector %s updated" % self.connector_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete connector from Masking engine and print status message
        return 0 if OK
        return 1 in case of error
        """

        api_instance = DatabaseConnectorApi(self.__engine.api_client)

        try:
            self.__logger.debug("delete connector id %s"
                                % self.environment_id)
            response = api_instance.delete_database_connector(
                self.database_connector_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("delete connector response %s"
                                % str(response))
            print_message("Connector %s deleted" % self.connector_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def test(self):
        """
        Test connector connection to database
        Return None if OK
        """

        api_instance = DatabaseConnectorApi(self.__engine.api_client)

        try:
            self.__logger.debug("test connector id %s"
                                % self.environment_id)
            response = api_instance.test_database_connector(
                self.database_connector_id,
                _request_timeout=self.__engine.get_timeout())
            if response.response == "Connection Failed":
                print_error("Connector test %s failed" % self.connector_name)
                return 1
            else:
                print_message("Connector test %s succeeded"
                              % self.connector_name)
                return 0
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

        api_instance = DatabaseConnectorApi(self.__engine.api_client)

        try:
            self.__logger.debug("fetch connector id %s"
                                % self.environment_id)
            response = api_instance.fetch_table_metadata(
                self.database_connector_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("list of tables" + str(response))
            return response
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return None
