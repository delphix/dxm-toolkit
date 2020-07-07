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

from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxConnector(object):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #DatabaseConnector.__init__(self)
        self.__is_database = None
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxConnector object")

        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.database_connector import DatabaseConnector
            from masking_api_60.api.database_connector_api import DatabaseConnectorApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.database_connector import DatabaseConnector
            from masking_api_53.api.database_connector_api import DatabaseConnectorApi
            from masking_api_53.rest import ApiException

        self.__api = DatabaseConnectorApi
        self.__model = DatabaseConnector
        self.__apiexc = ApiException
        self.__obj = None

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def database_connector_id(self):
        if self.__obj is not None:
            return self.__obj.database_connector_id
        else:
            return None

    @property
    def connectorId(self):
        if self.obj is not None:
            return self.obj.database_connector_id
        else:
            return None

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


    @property
    def connector_name(self):
        if self.obj is not None:
            return self.obj.connector_name
        else:
            return None     


    @property
    def database_type(self):
        if self.__obj is not None:
            return self.__obj.database_type
        else:
            return None     

    @property
    def environment_id(self):
        if self.obj is not None:
            return self.obj.environment_id
        else:
            return None     

    @property
    def custom_driver_name(self):
        if self.__obj is not None:
            return self.__obj.custom_driver_name
        else:
            return None    


    @property
    def database_name(self):
        if self.__obj is not None:
            return self.__obj.database_name
        else:
            return None    

    @database_name.setter
    def database_name(self, database_name):
        """
        database_name
        :param schemaName: database_name Name
        """

        if self.__obj is not None:
            self.__obj.database_name = database_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def host(self):
        if self.__obj is not None:
            return self.__obj.host
        else:
            return None  

    @host.setter
    def host(self, host):
        """
        host
        :param schemaName: host Name
        """

        if self.obj is not None:
            self.obj.host = host
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def instance_name(self):
        if self.__obj is not None:
            return self.__obj.instance_name
        else:
            return None  

    @instance_name.setter
    def instance_name(self, instance_name):
        """
        instance_name
        :param schemaName: instance_name Name
        """

        if self.__obj is not None:
            self.__obj.instance_name = instance_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def jdbc(self):
        if self.__obj is not None:
            return self.__obj.jdbc
        else:
            return None       

    @jdbc.setter
    def jdbc(self, jdbc):
        """
        jdbc
        :param schemaName: jdbc Name
        """

        if self.__obj is not None:
            self.__obj.jdbc = jdbc
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def port(self):
        if self.obj is not None:
            return self.obj.port
        else:
            return None  

    @port.setter
    def port(self, port):
        """
        port
        :param schemaName: port Name
        """

        if self.obj is not None:
            self.obj.port = port
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def schema_name(self):
        if self.__obj is not None:
            return self.__obj.schema_name
        else:
            return None  


    @schema_name.setter
    def schema_name(self, schema_name):
        """
        schema_name
        :param schemaName: schema_name Name
        """

        if self.__obj is not None:
            self.__obj.schema_name = schema_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def sid(self):
        if self.__obj is not None:
            return self.__obj.sid
        else:
            return None  


    @sid.setter
    def sid(self, sid):
        """
        sid
        :param schemaName: sid Name
        """

        if self.__obj is not None:
            self.__obj.sid = sid
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def username(self):
        if self.obj is not None:
            return self.obj.username
        else:
            return None  

    @username.setter
    def username(self, username):
        """
        username
        :param schemaName: username Name
        """

        if self.obj is not None:
            self.obj.username = username
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def password(self):
        if self.obj is not None:
            return 'xxxxxxxx'
        else:
            return None  

    @password.setter
    def password(self, password):
        """
        password
        :param schemaName: password Name
        """

        if self.obj is not None:
            self.obj.password = password
        else:
            raise ValueError("Object needs to be initialized first")

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



    def from_connector(self, con):
        """
        Set a obj property using a Database Connector 
        :param con: DatabaseConnector object
        """
        self.__obj = con

    def create_connector(self, connector_name, database_type, environment_id):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.__obj = self.__model(connector_name=connector_name, database_type=database_type, environment_id=environment_id)

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
        if hasattr(self.__obj, 'database_name'):
            if self.__obj.database_name is not None:
                props["database_name"] = self.__obj.database_name

        if hasattr(self.__obj, 'instance_name'):
            if self.__obj.instance_name is not None:
                props["instance_name"] = self.__obj.instance_name

        props["username"] = self.__obj.username

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
            self.__logger.debug("create connector input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_database_connector(
                self.__obj,
                _request_timeout=self.__engine.get_timeout())
            self.__obj = response

            self.__logger.debug("connector response %s"
                                % str(response))

            print_message("Connector %s added" % self.__obj.connector_name)
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
            # body added to workaround an issue with API 
            response = api_instance.test_database_connector(
                self.database_connector_id,
                body=self.obj,
                _request_timeout=self.__engine.get_timeout())
            if response.response == "Connection Failed":
                print_error("Connector test %s failed" % self.connector_name)
                return 1
            else:
                print_message("Connector test %s succeeded"
                              % self.connector_name)
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
