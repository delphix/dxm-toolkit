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

class DxConnector(object):

    swagger_types = {
        'database_connector_id': 'int',
        'connector_name': 'str',
        'database_type': 'str',
        'environment_id': 'int',
        'custom_driver_name': 'str',
        'database_name': 'str',
        'host': 'str',
        'instance_name': 'str',
        'jdbc': 'str',
        'password': 'str',
        'port': 'int',
        'schema_name': 'str',
        'sid': 'str',
        'username': 'str',
        'kerberos_auth': 'bool',
        'service_principal': 'str',
        'jdbc_driver_id': 'int',
        'enable_logger': 'bool',
        'file_reference_id': 'str'
    }

    swagger_map = {
        'database_connector_id': 'databaseConnectorId',
        'connector_name': 'connectorName',
        'database_type': 'databaseType',
        'environment_id': 'environmentId',
        'custom_driver_name': 'customDriverName',
        'database_name': 'databaseName',
        'host': 'host',
        'instance_name': 'instanceName',
        'jdbc': 'jdbc',
        'password': 'password',
        'port': 'port',
        'schema_name': 'schemaName',
        'sid': 'sid',
        'username': 'username',
        'kerberos_auth': 'kerberosAuth',
        'service_principal': 'servicePrincipal',
        'jdbc_driver_id': 'jdbcDriverId',
        'enable_logger': 'enableLogger',
        'file_reference_id': 'fileReferenceId'
    }


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
        self.__obj = None

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

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


    @property
    def database_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'database_connector_id'):
            return self.obj.database_connector_id
        else:
            return None

    @database_connector_id.setter
    def database_connector_id(self, database_connector_id):
        if self.obj is not None:
            self.obj.database_connector_id = database_connector_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def connector_name(self):
        if self.obj is not None and hasattr(self.obj,'connector_name'):
            return self.obj.connector_name
        else:
            return None

    @connector_name.setter
    def connector_name(self, connector_name):
        if self.obj is not None:
            self.obj.connector_name = connector_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def database_type(self):
        if self.obj is not None and hasattr(self.obj,'database_type'):
            return self.obj.database_type
        else:
            return None

    @database_type.setter
    def database_type(self, database_type):
        if self.obj is not None:
            self.obj.database_type = database_type
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def environment_id(self):
        if self.obj is not None and hasattr(self.obj,'environment_id'):
            return self.obj.environment_id
        else:
            return None

    @environment_id.setter
    def environment_id(self, environment_id):
        if self.obj is not None:
            self.obj.environment_id = environment_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def custom_driver_name(self):
        if self.obj is not None and hasattr(self.obj,'custom_driver_name'):
            return self.obj.custom_driver_name
        else:
            return None

    @custom_driver_name.setter
    def custom_driver_name(self, custom_driver_name):
        if self.obj is not None:
            self.obj.custom_driver_name = custom_driver_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def database_name(self):
        if self.obj is not None and hasattr(self.obj,'database_name'):
            return self.obj.database_name
        else:
            return None

    @database_name.setter
    def database_name(self, database_name):
        if self.obj is not None:
            self.obj.database_name = database_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def host(self):
        if self.obj is not None and hasattr(self.obj,'host'):
            return self.obj.host
        else:
            return None

    @host.setter
    def host(self, host):
        if self.obj is not None:
            self.obj.host = host
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def instance_name(self):
        if self.obj is not None and hasattr(self.obj,'instance_name'):
            return self.obj.instance_name
        else:
            return None

    @instance_name.setter
    def instance_name(self, instance_name):
        if self.obj is not None:
            self.obj.instance_name = instance_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def jdbc(self):
        if self.obj is not None and hasattr(self.obj,'jdbc'):
            return self.obj.jdbc
        else:
            return None

    @jdbc.setter
    def jdbc(self, jdbc):
        if self.obj is not None:
            self.obj.jdbc = jdbc
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def password(self):
        if self.obj is not None and hasattr(self.obj,'password'):
            return self.obj.password
        else:
            return None

    @password.setter
    def password(self, password):
        if self.obj is not None:
            self.obj.password = password
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def port(self):
        if self.obj is not None and hasattr(self.obj,'port'):
            return self.obj.port
        else:
            return None

    @port.setter
    def port(self, port):
        if self.obj is not None:
            self.obj.port = port
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def schema_name(self):
        if self.obj is not None and hasattr(self.obj,'schema_name'):
            return self.obj.schema_name
        else:
            return None

    @schema_name.setter
    def schema_name(self, schema_name):
        if self.obj is not None:
            self.obj.schema_name = schema_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def sid(self):
        if self.obj is not None and hasattr(self.obj,'sid'):
            return self.obj.sid
        else:
            return None

    @sid.setter
    def sid(self, sid):
        if self.obj is not None:
            self.obj.sid = sid
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def username(self):
        if self.obj is not None and hasattr(self.obj,'username'):
            return self.obj.username
        else:
            return None

    @username.setter
    def username(self, username):
        if self.obj is not None:
            self.obj.username = username
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def kerberos_auth(self):
        if self.obj is not None and hasattr(self.obj,'kerberos_auth'):
            return self.obj.kerberos_auth
        else:
            return None

    @kerberos_auth.setter
    def kerberos_auth(self, kerberos_auth):
        if self.obj is not None:
            self.obj.kerberos_auth = kerberos_auth
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def service_principal(self):
        if self.obj is not None and hasattr(self.obj,'service_principal'):
            return self.obj.service_principal
        else:
            return None

    @service_principal.setter
    def service_principal(self, service_principal):
        if self.obj is not None:
            self.obj.service_principal = service_principal
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def jdbc_driver_id(self):
        if self.obj is not None and hasattr(self.obj,'jdbc_driver_id'):
            return self.obj.jdbc_driver_id
        else:
            return None

    @jdbc_driver_id.setter
    def jdbc_driver_id(self, jdbc_driver_id):
        if self.obj is not None:
            self.obj.jdbc_driver_id = jdbc_driver_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def enable_logger(self):
        if self.obj is not None and hasattr(self.obj,'enable_logger'):
            return self.obj.enable_logger
        else:
            return None

    @enable_logger.setter
    def enable_logger(self, enable_logger):
        if self.obj is not None:
            self.obj.enable_logger = enable_logger
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def file_reference_id(self):
        if self.obj is not None and hasattr(self.obj,'file_reference_id'):
            return self.obj.file_reference_id
        else:
            return None

    @file_reference_id.setter
    def file_reference_id(self, file_reference_id):
        if self.obj is not None:
            self.obj.file_reference_id = file_reference_id
        else:
            raise ValueError("Object needs to be initialized first")


    def from_connector(self, con):
        """
        Set a obj property using a Database Connector 
        :param con: DatabaseConnector object
        """

        self.__obj = con
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map

    def create_connector(self, connector_name, database_type, environment_id):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.connector_name = connector_name
        self.database_type = database_type
        self.environment_id = environment_id


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
            self.__logger.debug("create connector input %s" % str(self.obj))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_database_connector(
                self.obj,
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