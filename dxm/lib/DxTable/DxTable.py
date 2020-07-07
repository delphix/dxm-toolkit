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


from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxTable(object):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #TableMetadata.__init__(self)
        self.__engine = engine
        self.__columnList = {}
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxTable object")
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.table_metadata import TableMetadata
            from masking_api_60.api.table_metadata_api import TableMetadataApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.table_metadata import TableMetadata
            from masking_api_53.api.table_metadata_api import TableMetadataApi
            from masking_api_53.rest import ApiException

        self.__api = TableMetadataApi
        self.__model = TableMetadata
        self.__apiexc = ApiException
        self.__obj = None

    def from_table(self, table):
        """
        Set obj object with real table object
        :param con: DatabaseConnector object
        """
        self.__obj = table

    def create_table(self, table_name, ruleset_id, custom_sql, where_clause, having_clause, key_column):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.__obj = self.__model(table_name=table_name, ruleset_id=ruleset_id, custom_sql=custom_sql, where_clause=where_clause, having_clause=having_clause, key_column=key_column)

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None


    @property
    def meta_name(self):
        return self.obj.table_name

    @property
    def meta_id(self):
        return self.obj.table_metadata_id

    @property
    def ruleset_id(self):
        return self.obj.ruleset_id

    @property
    def key_column(self):
        return self.obj.key_column

    @property
    def having_clause(self):
        return self.obj.having_clause

    @property
    def where_clause(self):
        return self.obj.where_clause

    @property
    def custom_sql(self):
        return self.obj.custom_sql

    def add(self):
        """
        Add table to Masking engine and print status message
        return 0 if non error
        return 1 in case of error
        """

        if (self.meta_name is None):
            print_error("Table name is required")
            self.__logger.error("Table name is required")
            return 1

        if (self.ruleset_id is None):
            print_error("ruleset_id is required")
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create table input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_table_metadata(self.obj)
            self.table_metadata_id = response.table_metadata_id

            self.__logger.debug("table response %s"
                                % str(response))

            print_message("Table %s added" % self.meta_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete table from ruleset
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.delete_table_metadata(self.obj.table_metadata_id)
            self.__logger.debug("table response %s"
                                % str(response))
            print_message("Table %s deleted" % self.obj.table_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update table on Masking engine
        return 0 if non error
        return 1 in case of error
        """

        try:
            self.__logger.debug("update table input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.update_table_metadata(
                self.obj.table_metadata_id,
                self.obj)
            self.__logger.debug("update table response %s"
                                % str(response))

            print_message("Table %s updated" % self.obj.table_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
