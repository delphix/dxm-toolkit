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

from dxm.lib.masking_api.api.file_format_api import FileFormatApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxFileFormat.FileFormat_mixin import FileFormat_mixin

class DxFileFormat(FileFormat_mixin):

    def __init__(self, engine, existing_object=None):
        """
        Constructor
        :param1 engine: DxMaskingEngine object
        :param2 execList: list of job executions
        """
        #FileFormat.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileFormat object")

        self.__api = FileFormatApi
        self.__apiexc = ApiException
        self._obj = None
        if existing_object is not None:
            self.load_object(existing_object)  


    def load_object(self, filetype):
        self.obj = filetype
        self.obj.swagger_types = self.swagger_types
        self.obj.swagger_map = self.swagger_map

    def create_fileformat(self, file_format_name, file_format_type):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.file_format_name = file_format_name
        self.obj.file_format_type = file_format_type



    def add(self):
        """
        Add File type to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.file_format_name is None):
            print_error("File format name is required")
            self.__logger.error("File format name is required")
            return 1

        if (self.obj.file_format_type is None):
            print_error("File format type is required")
            self.__logger.error("File format type is required")
            return 1

        try:
            self.__logger.debug("create filetype input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_file_format(self.obj.file_format_name,
                                                       self.obj.file_format_type)
            self.load_object(response)

            self.__logger.debug("filetype response %s"
                                % str(response))

            print_message("Filetype %s added" % self.obj.file_format_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete fiel format from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete file format id %s"
                                % self.obj.file_format_id)
            response = api_instance.delete_file_format(self.obj.file_format_id)
            self.__logger.debug("delete file format response %s"
                                % str(response))
            print_message("File format %s deleted" % self.obj.file_format_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
