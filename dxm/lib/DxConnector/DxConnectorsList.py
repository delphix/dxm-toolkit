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
import sys
from dxm.lib.DxConnector.OracleConnector import OracleConnector
from dxm.lib.DxConnector.MSSQLConnector import MSSQLConnector
from dxm.lib.DxConnector.SybaseConnector import SybaseConnector
from dxm.lib.DxConnector.DxFileConnector import DxFileConnector
from masking_apis.apis.database_connector_api import DatabaseConnectorApi
from masking_apis.apis.file_connector_api import FileConnectorApi
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList


class DxConnectorsList(object):

    __connectorsList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxConnectorsList object")

    @classmethod
    def LoadConnectors(self, environment_name):
        """
        Load all connectors
        :param1 environment_name: Limit load to particular environment name
        """

        # delete a list as we can have multi engines
        self.__connectorsList.clear()
        try:
            api_instance = DatabaseConnectorApi(self.__engine.api_client)

            if environment_name:
                environment_id = DxEnvironmentList.get_environmentId_by_name(
                                 environment_name)
                if environment_id:
                    dbconnectors = paginator(
                        api_instance,
                        "get_all_database_connectors",
                        environment_id=environment_id,
                        _request_timeout=self.__engine.get_timeout())
                else:
                    return 1

            else:
                environment_id = None
                dbconnectors = paginator(
                    api_instance,
                    "get_all_database_connectors",
                    _request_timeout=self.__engine.get_timeout())

            if dbconnectors.response_list:
                for c in dbconnectors.response_list:
                    if (c.database_type == 'ORACLE'):
                        connector = OracleConnector(self.__engine)
                    elif (c.database_type == 'MSSQL'):
                        connector = MSSQLConnector(self.__engine)
                    elif (c.database_type == 'SYBASE'):
                        connector = SybaseConnector(self.__engine)

                    connector.from_connector(c)
                    connector.is_database = True
                    self.__connectorsList['d' + str(c.database_connector_id)] \
                        = connector
            else:
                self.__logger.debug("No database connectors found")

            api_instance = FileConnectorApi(self.__engine.api_client)

            if environment_id:
                file_connectors = paginator(
                    api_instance,
                    "get_all_file_connectors",
                    environment_id=environment_id,
                    _request_timeout=self.__engine.get_timeout())
            else:
                file_connectors = paginator(
                    api_instance,
                    "get_all_file_connectors",
                    _request_timeout=self.__engine.get_timeout())

            if file_connectors.response_list:
                for f in file_connectors.response_list:
                    connector = DxFileConnector(self.__engine)
                    connector.from_connector(f)
                    connector.is_database = False
                    self.__connectorsList['f' + str(f.file_connector_id)] \
                        = connector
            else:
                self.__logger.debug("No file connectors found")

            if len(self.__connectorsList) < 1:
                print_error("No connectors found")
                self.__logger.error("No connectors found")
                return 1

            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a Connector object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__connectorsList[reference]

        except KeyError as e:
            self.__logger.debug("can't find Connector object"
                                " for reference %s" % reference)
            self.__logger.debug(e)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__connectorsList.keys()

    @classmethod
    def get_connectorId_by_name(self, name):
        """
        Return connector id by name.
        :param1 name: name of connector
        return ref if OK
        return None if ruleset not found or not unique
        """
        reflist = self.get_connectorId_by_name_worker(name)
        # convert list to single value
        # as there will be only one element in list
        if reflist:
            return reflist[0]
        else:
            return None

    @classmethod
    def get_all_connectorId_by_name(self, name):
        """
        Return all connector ids by name.
        :param1 name: name of connector
        return list of references if OK
        return None if ruleset not found
        """
        return self.get_connectorId_by_name_worker(name, None)

    @classmethod
    def get_connectorId_by_name_worker(self, name, check_uniquness=1):
        """
        Get a list of connectors by name
        :param1 name: name of connector
        :param2 check_uniqueness: check uniqueness put None if skip this check
        return list of connectors
        """
        connectors = get_objref_by_val_and_attribute(
            name, self, 'connector_name')

        if len(connectors) < 1:
            print_error("Connector %s not found" % name)
            self.__logger.error("Connector %s not found " % name)
            return None

        if check_uniquness:
            if len(connectors) > 1:
                print_error("Connector name %s is not unique" % name)
                self.__logger.error("Connector %s is not unique" % name)
                return None

        return connectors

    @classmethod
    def add(self, connector):
        """
        Add a connector to a list and Engine
        :param connector: Vendor connector object to add to Engine and list
        return None if OK
        """

        if (connector.add() is None):
            self.__logger.debug("Adding connector %s to list" % connector)
            self.__connectorsList[connector.database_connector_id] = connector
            return None
        else:
            return 1

    @classmethod
    def delete(self, databaseConnectorId):
        """
        Delete a connector from a list and Engine
        :param databaseConnectorId: Connector id to delete from Engine and list
        return None if OK
        """

        connector = self.get_by_ref(databaseConnectorId)
        if connector is not None:
            if connector.delete() is None:
                return None
            else:
                return 1
        else:
            print "Connector with id %s not found" % databaseConnectorId
            return 1
