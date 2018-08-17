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
# Date    : April 2018


import logging
from masking_apis.models.database_ruleset import DatabaseRuleset
from masking_apis.apis.database_ruleset_api import DatabaseRulesetApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxTable.DxTable import DxTable

class DxDatabaseRuleset(DatabaseRuleset):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DatabaseRuleset.__init__(self)
        self.__engine = engine
        self.__type = 'Database'
        self.__tableList = None
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxRuleset object")

    @property
    def type(self):
        return self.__type

    @property
    def ruleset_id(self):
        return self.database_ruleset_id

    @property
    def connectorId(self):
        return self.database_connector_id

    def from_ruleset(self, ruleset):
        """
        Copy properties from Ruleset object into DxRuleset
        :param con: DatabaseConnector object
        """
        self.__dict__.update(ruleset.__dict__)

    def add(self):
        """
        Add ruleset to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.ruleset_name is None):
            print "Ruleset name is required"
            self.__logger.error("Ruleset name is required")
            return 1

        if (self.database_connector_id is None):
            print "Database connector Id is required"
            self.__logger.error("Database connector ID is required")
            return 1

        try:
            self.__logger.debug("create database ruleset input %s" % str(self))

            api_instance = DatabaseRulesetApi(self.__engine.api_client)
            response = api_instance.create_database_ruleset(
                self,
                _request_timeout=self.__engine.get_timeout())
            self.database_ruleset_id = response.database_ruleset_id

            self.__logger.debug("ruleset response %s"
                                % str(response))

            print_message("Ruleset %s added" % self.ruleset_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete ruleset from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = DatabaseRulesetApi(self.__engine.api_client)

        try:
            self.__logger.debug("delete ruleset id %s"
                                % self.ruleset_id)
            response = api_instance.delete_database_ruleset(
                           self.ruleset_id,
                           _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("delete ruleset response %s"
                                % str(response))
            print_message("Ruleset %s deleted" % self.ruleset_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def addmeta(self, table_params):
        """
        Add table to ruleset
        :param table_params: set of table parametes
        return a None if non error
        return 1 in case of error
        """

        tablename = table_params["metaname"]
        custom_sql = table_params["custom_sql"]
        where_clause = table_params["where_clause"]
        having_clause = table_params["having_clause"]
        key_column = table_params["key_column"]

        if tablename is None:
            return 1

        table = DxTable(self.__engine)
        table.table_name = tablename
        table.ruleset_id = self.database_ruleset_id
        table.custom_sql = custom_sql
        table.where_clause = where_clause
        table.having_clause = having_clause
        table.key_column = key_column

        return table.add()

    def addmetafromfile(self, inputfile):
        """
        Add tables from file to ruleset
        :param inputfile: file with tables
        return a 0 if non error
        return 1 in case of error
        """
        ret = 0
        for line in inputfile:
            if line.startswith('#'):
                continue
            columns = line.strip().split(',')
            params = {
                "metaname": columns[0],
                "custom_sql": columns[1],
                "where_clause": columns[2],
                "having_clause": columns[3],
                "key_column": columns[4]
            }
            ret = ret + self.addmeta(params)

        return ret
