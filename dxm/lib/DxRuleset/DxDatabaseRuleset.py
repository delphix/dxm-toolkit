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
# Copyright (c) 2018-2020 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : April 2018


import logging
import re



from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxTable.DxTable import DxTable
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxAsyncTask.DxAsyncTask import DxAsyncTask
from dxm.lib.masking_api.api.database_ruleset_api import DatabaseRulesetApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxRuleset.DatabaseRuleset_mixin import DatabaseRuleset_mixin

class DxDatabaseRuleset(DatabaseRuleset_mixin):

    def __init__(self, engine, existing_object=None):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #DatabaseRuleset.__init__(self)
        self.__engine = engine
        self.__type = 'Database'
        self.__tableList = None
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxRuleset object")


        self.__api = DatabaseRulesetApi
        self.__apiexc = ApiException
        self._obj = None

        if existing_object is not None:
            self.load_object(existing_object)   


    @property
    def type(self):
        return self.__type

    @property
    def ruleset_id(self):
        return self.obj.database_ruleset_id


    @property
    def connectorId(self):
        return 'd' + str(self.obj.database_connector_id)

    def load_object(self, ruleset):
        """
        Set obj object with real ruleset object
        :param con: DatabaseConnector object
        """
        self.obj = ruleset
        self.obj.swagger_types = self.swagger_types
        self.obj.swagger_map = self.swagger_map

    @property
    def logger(self):
        return self.__logger

    @property
    def engine(self):
        return self.__engine

    def create_database_ruleset(self, ruleset_name, database_connector_id, refresh_drops_tables):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.ruleset_name = ruleset_name
        self.obj.database_connector_id = database_connector_id
        self.obj.refresh_drops_tables = refresh_drops_tables



    def add(self):
        """
        Add ruleset to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.ruleset_name is None):
            print_error("Ruleset name is required")
            self.__logger.error("Ruleset name is required")
            return 1

        if (self.obj.database_connector_id is None):
            print_error("Database connector Id is required")
            self.__logger.error("Database connector ID is required")
            return 1

        try:
            self.logger.debug("create database ruleset input %s" % str(self))

            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_database_ruleset(
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.obj = response

            self.logger.debug("ruleset response %s"
                                % str(response))

            print_message("Ruleset %s added" % self.ruleset_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.logger.error(e)
            return 1

    def delete(self):
        """
        Delete ruleset from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.logger.debug("delete ruleset id %s"
                                % self.ruleset_id)
            response = api_instance.delete_database_ruleset(
                           self.ruleset_id,
                           _request_timeout=self.__engine.get_timeout())
            self.logger.debug("delete ruleset response %s"
                                % str(response))
            print_message("Ruleset %s deleted" % self.ruleset_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.logger.error(e)
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
        table.create_table(
            table_name = tablename,
            ruleset_id = self.ruleset_id,
            custom_sql = custom_sql,
            where_clause = where_clause,
            having_clause = having_clause,
            key_column = key_column
        )

        return table.add()

    def addmetafromfile(self, inputfile, bulk):
        """
        Add tables from file to ruleset
        :param inputfile: file with tables
        return a 0 if non error
        return 1 in case of error
        """
        ret = 0
        table_list = []
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
            if bulk:
                table_list.append(params)
            else:
                ret = ret + self.addmeta(params)

        if bulk:
            ret = self.addmeta_bulk(table_list)

        return ret


    def addmetafromfetch(self, fetchfilter, bulk):
        """
        Add tables from fetch into ruleset
        :param fetchfilter: filter for tables
        return a 0 if non error
        return 1 in case of error
        """
        
        connobj = DxConnectorsList.get_by_ref(self.connectorId)
        table_list = []
        ret = 0

        if fetchfilter:
            fetchfilter = re.escape(fetchfilter).replace("\*",".*")
            self.logger.debug("fetchfilter {}".format(fetchfilter))
            pattern = re.compile(r'^{}$'.format(fetchfilter))

        for table in connobj.fetch_meta():
            params = {
                "metaname": table,
                "custom_sql": None,
                "where_clause": None,
                "having_clause": None,
                "key_column": None
            }

            self.logger.debug("checking table {}".format(table))

            if fetchfilter:
                if pattern.search(table):
                    self.logger.debug("filtered table added to bulk{}".format(table))
                    if bulk:
                        table_list.append(params)
                    else:
                        ret = ret + self.addmeta(params)
            else:
                    if bulk:
                        table_list.append(params)
                    else:
                        ret = ret + self.addmeta(params)            

        # TODO: 
        # add check of version of fail before trying 

        if bulk:
            ret = self.addmeta_bulk(table_list)
        
        return ret



    def create_bulk_objects(self, table_list):
            swagger_types = {
                'table_metadata': 'list[TableMetadata]'
            }

            swagger_map = {
                'table_metadata': 'tableMetadata'
            }

            obj = GenericModel({ x:None for x in self.swagger_map.values()}, swagger_types, swagger_map)
            obj.table_metadata = table_list
            return obj


    def addmeta_bulk(self, table_list):
        """

        """
        
        table_obj_list = []
        
        for table_params in table_list:
            table = DxTable(self.engine)
            table.create_table(
                table_name = table_params["metaname"],
                ruleset_id = self.ruleset_id,
                custom_sql = table_params["custom_sql"],
                where_clause = table_params["where_clause"],
                having_clause = table_params["having_clause"],
                key_column = table_params["key_column"]
            )

            table_obj_list.append(table.obj)
        
        table_bulk = self.create_bulk_objects(table_obj_list)        
        api_instance = self.__api(self.__engine.api_client)
        
        try:
            self.logger.debug("create bulk %s"
                                % self.ruleset_id)
            self.logger.debug("create bulk tables %s"
                                % str(table_bulk))
            response = api_instance.bulk_table_update(
                           self.ruleset_id,
                           table_bulk,
                           _request_timeout=self.__engine.get_timeout())
            self.logger.debug("create bulk response %s"
                                % str(response))
            print_message("Ruleset %s update started" % self.ruleset_name)

            task = DxAsyncTask()
            task.from_asynctask(response)
            return task.wait_for_task()
        except self.__apiexc as e:
            print_error(e.body)
            self.logger.error(e)
            return 1

    def refresh(self):
        """
        Refresh ruleset on the Masking engine 
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("refresh ruleset id %s"
                                % self.ruleset_id)
            response = api_instance.refresh_database_ruleset(
                           self.ruleset_id,
                           _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("refresh ruleset response %s"
                                % str(response))
            print_message("Ruleset %s refresh started" % self.ruleset_name)

            task = DxAsyncTask()
            task.from_asynctask(response)
            return task.wait_for_task()
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    def copy(self, newname):
        """
        Copy ruleset on the Masking engine 
        newname - name of the new ruleset
        return a new ruleset if non error
        return None if error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("copy ruleset id %s"
                                % self.ruleset_id)
            response = api_instance.refresh_database_ruleset(
                           self.ruleset_id,
                           _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("refresh ruleset response %s"
                                % str(response))
            print_message("Ruleset %s refresh started" % self.ruleset_name)

            task = DxAsyncTask()
            task.from_asynctask(response)
            return task.wait_for_task()
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1