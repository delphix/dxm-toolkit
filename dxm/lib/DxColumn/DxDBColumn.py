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
class DxDBColumn(object):

    swagger_types = {
        'column_metadata_id': 'int',
        'column_name': 'str',
        'table_metadata_id': 'int',
        'algorithm_name': 'str',
        'domain_name': 'str',
        'data_type': 'str',
        'date_format': 'str',
        'column_length': 'int',
        'is_masked': 'bool',
        'is_profiler_writable': 'bool',
        'is_primary_key': 'bool',
        'is_index': 'bool',
        'is_foreign_key': 'bool',
        'notes': 'str',
        'algorithm_field_id': 'int',
        'algorithm_group_no': 'int'
    }

    swagger_map = {
        'column_metadata_id': 'columnMetadataId',
        'column_name': 'columnName',
        'table_metadata_id': 'tableMetadataId',
        'algorithm_name': 'algorithmName',
        'domain_name': 'domainName',
        'data_type': 'dataType',
        'date_format': 'dateFormat',
        'column_length': 'columnLength',
        'is_masked': 'isMasked',
        'is_profiler_writable': 'isProfilerWritable',
        'is_primary_key': 'isPrimaryKey',
        'is_index': 'isIndex',
        'is_foreign_key': 'isForeignKey',
        'notes': 'notes',
        'algorithm_field_id': 'algorithmFieldId',
        'algorithm_group_no': 'algorithmGroupNo'
    }

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #ColumnMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxDBColumn object")

        self.__api = ColumnMetadataApi
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
        if hasattr(column, "notes") and column.notes == 'N/A':
            column.notes = None

        self.__obj = column
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map


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
    def column_metadata_id(self):
        if self.obj is not None and hasattr(self.obj,'column_metadata_id'):
            return self.obj.column_metadata_id
        else:
            return None

    @column_metadata_id.setter
    def column_metadata_id(self, column_metadata_id):
        if self.obj is not None:
            self.obj.column_metadata_id = column_metadata_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def column_name(self):
        if self.obj is not None and hasattr(self.obj,'column_name'):
            return self.obj.column_name
        else:
            return None

    @column_name.setter
    def column_name(self, column_name):
        if self.obj is not None:
            self.obj.column_name = column_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def table_metadata_id(self):
        if self.obj is not None and hasattr(self.obj,'table_metadata_id'):
            return self.obj.table_metadata_id
        else:
            return None

    @table_metadata_id.setter
    def table_metadata_id(self, table_metadata_id):
        if self.obj is not None:
            self.obj.table_metadata_id = table_metadata_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def algorithm_name(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_name'):
            return self.obj.algorithm_name
        else:
            return None

    @algorithm_name.setter
    def algorithm_name(self, algorithm_name):
        if self.obj is not None:
            self.obj.algorithm_name = algorithm_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def domain_name(self):
        if self.obj is not None and hasattr(self.obj,'domain_name'):
            return self.obj.domain_name
        else:
            return None

    @domain_name.setter
    def domain_name(self, domain_name):
        if self.obj is not None:
            self.obj.domain_name = domain_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def data_type(self):
        if self.obj is not None and hasattr(self.obj,'data_type'):
            return self.obj.data_type
        else:
            return None

    @data_type.setter
    def data_type(self, data_type):
        if self.obj is not None:
            self.obj.data_type = data_type
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def date_format(self):
        if self.obj is not None and hasattr(self.obj,'date_format'):
            return self.obj.date_format
        else:
            return None

    @date_format.setter
    def date_format(self, date_format):
        if self.obj is not None:
            self.obj.date_format = date_format
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def column_length(self):
        if self.obj is not None and hasattr(self.obj,'column_length'):
            return self.obj.column_length
        else:
            return None

    @column_length.setter
    def column_length(self, column_length):
        if self.obj is not None:
            self.obj.column_length = column_length
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def is_masked(self):
        if self.obj is not None and hasattr(self.obj,'is_masked'):
            return self.obj.is_masked
        else:
            return None

    @is_masked.setter
    def is_masked(self, is_masked):
        if self.obj is not None:
            self.obj.is_masked = is_masked
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def is_profiler_writable(self):
        if self.obj is not None and hasattr(self.obj,'is_profiler_writable'):
            return self.obj.is_profiler_writable
        else:
            return None

    @is_profiler_writable.setter
    def is_profiler_writable(self, is_profiler_writable):
        if self.obj is not None:
            self.obj.is_profiler_writable = is_profiler_writable
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def is_primary_key(self):
        if self.obj is not None and hasattr(self.obj,'is_primary_key'):
            return self.obj.is_primary_key
        else:
            return None

    @is_primary_key.setter
    def is_primary_key(self, is_primary_key):
        if self.obj is not None:
            self.obj.is_primary_key = is_primary_key
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def is_index(self):
        if self.obj is not None and hasattr(self.obj,'is_index'):
            return self.obj.is_index
        else:
            return None

    @is_index.setter
    def is_index(self, is_index):
        if self.obj is not None:
            self.obj.is_index = is_index
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def is_foreign_key(self):
        if self.obj is not None and hasattr(self.obj,'is_foreign_key'):
            return self.obj.is_foreign_key
        else:
            return None

    @is_foreign_key.setter
    def is_foreign_key(self, is_foreign_key):
        if self.obj is not None:
            self.obj.is_foreign_key = is_foreign_key
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def notes(self):
        if self.obj is not None and hasattr(self.obj,'notes'):
            return self.obj.notes
        else:
            return None

    @notes.setter
    def notes(self, notes):
        if self.obj is not None:
            self.obj.notes = notes
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def algorithm_field_id(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_field_id'):
            return self.obj.algorithm_field_id
        else:
            return None

    @algorithm_field_id.setter
    def algorithm_field_id(self, algorithm_field_id):
        if self.obj is not None:
            self.obj.algorithm_field_id = algorithm_field_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def algorithm_group_no(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_group_no'):
            return self.obj.algorithm_group_no
        else:
            return None

    @algorithm_group_no.setter
    def algorithm_group_no(self, algorithm_group_no):
        if self.obj is not None:
            self.obj.algorithm_group_no = algorithm_group_no
        else:
            raise ValueError("Object needs to be initialized first")

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
