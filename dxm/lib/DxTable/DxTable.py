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
from masking_apis.models.table_metadata import TableMetadata
from masking_apis.apis.table_metadata_api import TableMetadataApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxTable(TableMetadata):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        TableMetadata.__init__(self)
        self.__engine = engine
        self.__columnList = {}
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxTable object")

    def from_table(self, table):
        """
        Copy properties from Ruleset object into DxRuleset
        :param con: DatabaseConnector object
        """
        self.__dict__.update(table.__dict__)

    @property
    def meta_name(self):
        return self.table_name

    @property
    def meta_id(self):
        return self.table_metadata_id

    def add(self):
        """
        Add table to Masking engine and print status message
        return 0 if non error
        return 1 in case of error
        """

        if (self.table_name is None):
            print "Table name is required"
            self.__logger.error("Table name is required")
            return 1

        if (self.ruleset_id is None):
            print "ruleset_id is required"
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create table input %s" % str(self))
            api_instance = TableMetadataApi(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_table_metadata(self)
            self.table_metadata_id = response.table_metadata_id

            self.__logger.debug("table response %s"
                                % str(response))

            print_message("Table %s added" % self.table_name)
            return 0
        except ApiException as e:
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
            api_instance = TableMetadataApi(self.__engine.api_client)
            response = api_instance.delete_table_metadata(self.table_metadata_id)
            self.__logger.debug("table response %s"
                                % str(response))
            print_message("Table %s deleted" % self.table_name)
            return 0
        except ApiException as e:
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
            api_instance = TableMetadataApi(self.__engine.api_client)
            response = api_instance.update_table_metadata(
                self.table_metadata_id,
                self)
            self.__logger.debug("update table response %s"
                                % str(response))

            print_message("Table %s updated" % self.table_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
