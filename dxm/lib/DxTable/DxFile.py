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
from masking_apis.models.file_metadata import FileMetadata
from masking_apis.apis.file_metadata_api import FileMetadataApi
from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxFile(FileMetadata):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        FileMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFile object")
        self.file_format_id

    def from_file(self, file):
        """
        Copy properties from file object into Dxfile
        :param file: FileMetadata object
        """
        self.__dict__.update(file.__dict__)

    @property
    def meta_name(self):
        return self.file_name

    @property
    def meta_id(self):
        return self.file_metadata_id

    @FileMetadata.file_format_id.setter
    def file_format_id(self, file_name):
        fileformatList = DxFileFormatList()
        fileformat = fileformatList.get_file_format_id_by_name(file_name)
        if fileformat:
            self._file_format_id = fileformat
        else:
            self._file_format_id = None

    @FileMetadata.end_of_record.setter
    def end_of_record(self, eor):
        eor_string = None
        if eor is None:
            eor_string = None
        else:
            if eor == 'linux':
                eor_string = '\n'
            elif eor == 'windows':
                eor_string = '\r\n'
            elif len(eor) > 0:
                eor_string = eor

        if eor_string:
            self._end_of_record = eor_string
        else:
            self._end_of_record = None

    def add(self):
        """
        Add table to Masking engine and print status message
        return 0 if non error
        return 1 in case of error
        """

        if (self.file_name is None):
            print "File name is required"
            self.__logger.error("File name is required")
            return 1

        if (self.ruleset_id is None):
            print "ruleset_id is required"
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create file input %s" % str(self))
            api_instance = FileMetadataApi(self.__engine.api_client)
            response = api_instance.create_file_metadata(self)
            self.file_metadata_id = response.file_metadata_id

            self.__logger.debug("file response %s"
                                % str(response))

            print_message("File %s added" % self.file_name)
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
            api_instance = FileMetadataApi(self.__engine.api_client)
            response = api_instance.delete_file_metadata(self.file_metadata_id)
            self.__logger.debug("file response %s"
                                % str(response))
            print_message("File %s deleted" % self.file_name)
            return 0
        except ApiException as e:
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
            api_instance = FileMetadataApi(self.__engine.api_client)
            response = api_instance.update_file_metadata(
                self.file_metadata_id,
                self)
            self.__logger.debug("update file response %s"
                                % str(response))

            print_message("File %s updated" % self.file_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
