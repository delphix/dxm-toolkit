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

from dxm.lib.masking_api.api.file_field_metadata_api import FileFieldMetadataApi
from dxm.lib.masking_api.rest import ApiException

class DxFileField(object):


    swagger_types = {
        'file_field_metadata_id': 'int',
        'file_format_id': 'int',
        'record_type_id': 'int',
        'field_length': 'int',
        'field_name': 'str',
        'field_position_number': 'int',
        'algorithm_name': 'str',
        'domain_name': 'str',
        'date_format': 'str',
        'is_masked': 'bool',
        'is_profiler_writable': 'bool',
        'notes': 'str'
    }

    swagger_map = {
        'file_field_metadata_id': 'fileFieldMetadataId',
        'file_format_id': 'fileFormatId',
        'record_type_id': 'recordTypeId',
        'field_length': 'fieldLength',
        'field_name': 'fieldName',
        'field_position_number': 'fieldPositionNumber',
        'algorithm_name': 'algorithmName',
        'domain_name': 'domainName',
        'date_format': 'dateFormat',
        'is_masked': 'isMasked',
        'is_profiler_writable': 'isProfilerWritable',
        'notes': 'notes'
    }

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #FileFieldMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFile object")

        self.__api = FileFieldMetadataApi
        self.__obj = None
        self.__apiexc = ApiException



    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    def from_file(self, file):
        """
        set obj property with FileMetadata object
        :param column: FileMetadata object
        """
        self.__obj = file
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map

    @property
    def cf_meta_name(self):
        return self.obj.field_name

    @property
    def cf_metadata_id(self):
        return self.obj.file_field_metadata_id

    @property
    def cf_meta_type(self):
        if self.obj.field_length == 0 or self.obj.field_length is None:
            return "pos {}".format(self.obj.field_position_number)
        else:
            return "pos {} ({})".format(self.obj.field_position_number,
                                        self.obj.field_length)

    @property
    def cf_meta_column_role(self):
        return ''

    @property
    def algorithm_name(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_name'):
            return self.__obj.algorithm_name
        else:
            return None

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

    def update(self):
        """
        Update file field data to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.file_field_metadata_id is None):
            print_error("file_field_metadata_id is required")
            self.__logger.error("file_field_metadata_id is required")
            return 1

        try:
            if self.obj.date_format == '':
                self.date_format = None

            self.__logger.debug("create field input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.update_file_field_metadata(self.obj.file_field_metadata_id, self.obj)
            self.__logger.debug("field response %s"
                                % str(response))

            print_message("Field %s updated" % self.obj.field_name)
            return None
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
