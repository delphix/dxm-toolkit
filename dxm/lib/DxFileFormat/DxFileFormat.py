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
from masking_apis.models.file_format import FileFormat
from masking_apis.apis.file_format_api import FileFormatApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxFileFormat(FileFormat):

    def __init__(self, engine):
        """
        Constructor
        :param1 engine: DxMaskingEngine object
        :param2 execList: list of job executions
        """
        FileFormat.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileFormat object")

    def from_filetype(self, filetype):
        """
        Copy properties from MaskingJob object into DxFiletype
        :param con: MaskingJob object
        """
        self.__dict__.update(filetype.__dict__)

    def add(self):
        """
        Add File type to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.file_format_name is None):
            print_error("File format name is required")
            self.__logger.error("File format name is required")
            return 1

        if (self.file_format_type is None):
            print_error("File format type is required")
            self.__logger.error("File format type is required")
            return 1

        try:
            self.__logger.debug("create filetype input %s" % str(self))
            api_instance = FileFormatApi(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_file_format(self.file_format_name,
                                                       self.file_format_type)
            self.from_filetype(response)

            self.__logger.debug("filetype response %s"
                                % str(response))

            print_message("Filetype %s added" % self.file_format_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete fiel format from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = FileFormatApi(self.__engine.api_client)

        try:
            self.__logger.debug("delete file format id %s"
                                % self.file_format_id)
            response = api_instance.delete_file_format(self.file_format_id)
            self.__logger.debug("delete file format response %s"
                                % str(response))
            print_message("File format %s deleted" % self.file_format_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
