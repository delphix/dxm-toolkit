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

from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxFile(object):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #FileMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFile object")
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.file_metadata import FileMetadata
            from masking_api_60.api.file_metadata_api import FileMetadataApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.file_metadata import FileMetadata
            from masking_api_53.api.file_metadata_api import FileMetadataApi
            from masking_api_53.rest import ApiException

        self.__api = FileMetadataApi
        self.__model = FileMetadata
        self._apiexc = ApiException
        self.__obj = None

    def from_file(self, file):
        """
        Set obj object with real table object
        :param file: FileMetadata object
        """
        self.__obj = file

    def create_file(self, file_name, ruleset_id, file_format_id, file_type, delimiter, enclosure, end_of_record, name_is_regular_expression):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        fileformatList = DxFileFormatList()
        fileformat_id = fileformatList.get_file_format_id_by_name(file_format_id)

        eor_string = None
        if end_of_record is None:
            eor_string = None
        else:
            if end_of_record == 'linux':
                eor_string = '\n'
            elif end_of_record == 'windows':
                eor_string = '\r\n'
            elif len(end_of_record) > 0:
                eor_string = end_of_record

        self.__obj = self.__model(file_name=file_name, ruleset_id=ruleset_id, file_format_id=fileformat_id, 
                                  file_type=file_type, delimiter=delimiter, enclosure=enclosure, end_of_record=eor_string, 
                                  name_is_regular_expression=name_is_regular_expression)


    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def meta_name(self):
        return self.obj.file_name

    @property
    def meta_id(self):
        return self.obj.file_metadata_id

    @property
    def file_format_id(self):
        return self.obj.file_format_id


    @property
    def end_of_record(self):
        return self.obj.end_of_record

    @property
    def file_type(self):
        return self.obj.file_type

    @property
    def delimiter(self):
        return self.obj.delimiter

    @property
    def enclosure(self):
        return self.obj.enclosure

    @property
    def name_is_regular_expression(self):
        return self.obj.name_is_regular_expression

    def add(self):
        """
        Add table to Masking engine and print status message
        return 0 if non error
        return 1 in case of error
        """

        if (self.obj.file_name is None):
            print_error("File name is required")
            self.__logger.error("File name is required")
            return 1

        if (self.obj.ruleset_id is None):
            print_error("ruleset_id is required")
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create file input %s" % str(self.obj))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_file_metadata(self.obj)
            self.__obj = response

            self.__logger.debug("file response %s"
                                % str(response))

            print_message("File %s added" % self.obj.file_name)
            return 0
        except self._apiexc as e:
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
            response = api_instance.delete_file_metadata(self.obj.file_metadata_id)
            self.__logger.debug("file response %s"
                                % str(response))
            print_message("File %s deleted" % self.obj.file_name)
            return 0
        except self._apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update file on Masking engine
        return 0 if non error
        return 1 in case of error
        """

        try:
            self.__logger.debug("update table input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.update_file_metadata(
                self.obj.file_metadata_id,
                self.obj)
            self.__logger.debug("update file response %s"
                                % str(response))

            print_message("File %s updated" % self.obj.file_name)
            return 0
        except self._apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
