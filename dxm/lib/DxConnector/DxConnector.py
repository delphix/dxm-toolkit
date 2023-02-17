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
import pprint

from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

from dxm.lib.masking_api.api.database_connector_api import DatabaseConnectorApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxConnector.DatabaseConnector_mixin import DatabaseConnector_mixin

class DxConnector(DatabaseConnector_mixin):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__is_database = None
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxConnector object")
        self.__api = DatabaseConnectorApi
        self.__apiexc = ApiException
        self.obj = None



    @property
    def connectorId(self):
        if self.obj is not None:
            return self.obj.database_connector_id
        else:
            return None

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

    @property
    def connector_type(self):
        """
        connector_type
        """
        if self.obj is not None:
            if self.is_database:
                return self.obj.database_type
            else:
                return self.obj.file_type
        else:
            return None


    def from_connector(self, con):
        """
        Set a obj property using a Database Connector 
        :param con: DatabaseConnector object
        """

        self.obj = con


    def create_connector(self, connector_name, database_type, environment_id):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.connector_name = connector_name
        self.database_type = database_type
        self.environment_id = environment_id
        self.is_database = True
        self.obj.swagger_types = self.swagger_types
        self.obj.swagger_map = self.swagger_map


    def get_properties(self):
        """
        get_properties is abstract method - implement in vendor class
        if there is no vendor class - checks will be done by API of engine
        """
        return {}

    def get_type_properties(self):
        """
        Return dict with generic properties
        """
        props = {}
        if hasattr(self.obj, 'database_name'):
            if self.obj.database_name is not None:
                props["database_name"] = self.obj.database_name

        if hasattr(self.obj, 'instance_name'):
            if self.obj.instance_name is not None:
                props["instance_name"] = self.obj.instance_name

        props["username"] = self.obj.username

        return props

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
            self.__logger.debug("create connector input %s" % str(self.obj))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_database_connector(
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.obj = response
            self.obj.swagger_types = self.swagger_types
            self.obj.swagger_map = self.swagger_map
            self.__logger.debug("connector response %s"
                                % str(response))

            print_message("Connector %s added" % self.obj.connector_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    def update(self):
        """
        Update connector on engine
        Return None if OK
        """

        api_instance = self.__api(self.__engine.api_client)
        # body = DatabaseConnector()

        # for k in self.attribute_map.keys():
        #     if getattr(self, k) is not None:
        #         setattr(body, k, getattr(self, k))

        try:
            self.__logger.debug("update connector input %s" % str(self))
            response = api_instance.update_database_connector(
                self.database_connector_id,
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("update connector response %s"
                                % str(response))

            #self.database_connector_id = response.database_connector_id
            print_message("Connector %s updated" % self.connector_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete connector from Masking engine and print status message
        return 0 if OK
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

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
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def test(self):
        """
        Test connector connection to database
        Return None if OK
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("test connector id %s"
                                % self.database_connector_id)
            self.__logger.debug("body {}".format(str(self.obj)))
            # body added to workaround an issue with API 
            response = api_instance.test_database_connector(
                self.database_connector_id,
                body=self.obj,
                _request_timeout=self.__engine.get_timeout())

            if "Connection Failed" in response.response:
                print_error("Connector test {} failed. Error message is: {}".format(self.connector_name, response.response))
                return 1
            else:
                print_message("Connector test {} succeeded".format(self.connector_name))
                return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def fetch_meta(self):
        """
        Fetch list of tables
        Return list if OK
        None if no objects
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("fetch connector id %s"
                                % self.environment_id)
            response = api_instance.fetch_table_metadata(
                self.database_connector_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("list of tables" + str(response))
            return response
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return None

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()