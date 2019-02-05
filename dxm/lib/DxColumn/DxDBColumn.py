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
from masking_apis.apis.column_metadata_api import ColumnMetadataApi
from masking_apis.models.column_metadata import ColumnMetadata
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxDBColumn(ColumnMetadata):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        ColumnMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxDBColumn object")

    def from_column(self, column):
        """
        Copy properties from column object into DxDBColumn
        :param column: ColumnMetadata object
        """
        self.__dict__.update(column.__dict__)

    @property
    def cf_metadata_id(self):
        return self.column_metadata_id

    @property
    def cf_meta_name(self):
        return self.column_name

    @property
    def cf_meta_type(self):
        if self.column_length == 0:
            return "{}".format(self.data_type)
        else:
            return "{}({})".format(self.data_type, self.column_length)

    @property
    def cf_meta_column_role(self):
        ret = ''
        if self.is_primary_key:
            ret = 'PK '

        if self.is_foreign_key:
            ret = ret + "FK "

        if self.is_index:
            ret = ret + "IX "

        return ret.strip()

    def update(self):
        """
        Update column data to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.column_metadata_id is None):
            print "column_metadata_id is required"
            self.__logger.error("column_metadata_id is required")
            return 1

        try:
            if self.date_format == '':
                self.date_format = None

            self.__logger.debug("create column input %s" % str(self))
            api_instance = ColumnMetadataApi(self.__engine.api_client)
            response = api_instance.update_column_metadata(self.column_metadata_id, self)
            self.__logger.debug("column response %s"
                                % str(response))

            print_message("Column %s updated" % self.column_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
