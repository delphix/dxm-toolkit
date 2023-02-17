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
import pprint
import json


from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

from dxm.lib.masking_api.api.column_metadata_api import ColumnMetadataApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxColumn.ColumnMetadata_mixin import ColumnMetadata_mixin
class DxDBColumn(ColumnMetadata_mixin):



    def __init__(self, engine, existing_object=None):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #ColumnMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxDBColumn object")

        self.__api = ColumnMetadataApi
        self._obj = None
        self.__apiexc = ApiException

        if existing_object is not None:
            self.load_object(existing_object)   


    def load_object(self, column):
        """
        set obj property with ColumnMetadata object
        :param column: ColumnMetadata object
        """
        if hasattr(column, "notes") and column.notes == 'N/A':
            column.notes = None

        self.obj = column
        self.obj.swagger_types = self.swagger_types
        self.obj.swagger_map = self.swagger_map


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



    def update(self):
        """
        Update column data to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.column_metadata_id is None):
            print_error("column_metadata_id is required")
            self.__logger.error("column_metadata_id is required")
            return 1

        try:
            if self.date_format == '':
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

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()
