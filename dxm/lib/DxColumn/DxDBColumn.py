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


class DxDBColumn(object):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #ColumnMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxDBColumn object")
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.api.column_metadata_api import ColumnMetadataApi
            from masking_api_60.models.column_metadata import ColumnMetadata
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.api.column_metadata_api import ColumnMetadataApi
            from masking_api_53.models.column_metadata import ColumnMetadata
            from masking_api_53.rest import ApiException

        self.__api = ColumnMetadataApi
        self.__model = ColumnMetadata
        self.__obj = None
        self.__apiexc = ApiException


    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    def from_column(self, column):
        """
        set obj property with ColumnMetadata object
        :param column: ColumnMetadata object
        """
        self.__obj = column

    @property
    def cf_metadata_id(self):
        return self.obj.column_metadata_id

    @property
    def cf_meta_name(self):
        return self.obj.column_name

    @property
    def cf_meta_type(self):
        if self.obj.column_length == 0:
            return "{}".format(self.obj.data_type)
        else:
            return "{}({})".format(self.obj.data_type, self.obj.column_length)

    @property
    def cf_meta_column_role(self):
        ret = ''
        if self.obj.is_primary_key:
            ret = 'PK '

        if self.obj.is_foreign_key:
            ret = ret + "FK "

        if self.obj.is_index:
            ret = ret + "IX "

        return ret.strip()


    @property
    def algorithm_name(self):
        return self.obj.algorithm_name

    @algorithm_name.setter
    def algorithm_name(self, algorithm_name):
        """
        algorithm_name
        :param algorithm_name: algorithm_name 
        """

        if self.obj is not None:
            self.obj.algorithm_name = algorithm_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def domain_name(self):
        return self.obj.domain_name

    @domain_name.setter
    def domain_name(self, domain_name):
        """
        domain_name
        :param domain_name: domain_name 
        """

        if self.obj is not None:
            self.obj.domain_name = domain_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def is_masked(self):
        return self.obj.is_masked

    @is_masked.setter
    def is_masked(self, is_masked):
        """
        is_masked
        :param is_masked: is_masked flag
        """

        if self.obj is not None:
            self.obj.is_masked = is_masked
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def is_profiler_writable(self):
        return self.obj.is_profiler_writable

    def update(self):
        """
        Update column data to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.column_metadata_id is None):
            print_error("column_metadata_id is required")
            self.__logger.error("column_metadata_id is required")
            return 1

        try:
            if self.obj.date_format == '':
                self.date_format = None

            self.__logger.debug("create column input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.update_column_metadata(self.obj.column_metadata_id, self.obj)
            self.__logger.debug("column response %s"
                                % str(response))

            print_message("Column %s updated" % self.obj.column_name)
            return None
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
