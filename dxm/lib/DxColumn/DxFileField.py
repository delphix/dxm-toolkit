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
from dxm.lib.DxColumn.FileFieldMetadata_mixin import FileFieldMetadata_mixin

class DxFileField(FileFieldMetadata_mixin):



    def __init__(self, engine, existing_object=None):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #FileFieldMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFile object")

        self.__api = FileFieldMetadataApi
        self._obj = None
        self.__apiexc = ApiException

        if existing_object is not None:
            self.load_object(existing_object)  



    def load_object(self, file):
        """
        set obj property with FileMetadata object
        :param column: FileMetadata object
        """
        self.obj = file
        self.obj.swagger_types = self.swagger_types
        self.obj.swagger_map = self.swagger_map

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
