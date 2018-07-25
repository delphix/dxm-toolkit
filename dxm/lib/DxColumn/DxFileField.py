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
from masking_apis.models.file_field_metadata import FileFieldMetadata
from masking_apis.apis.file_field_metadata_api import FileFieldMetadataApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxFileField(FileFieldMetadata):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        FileFieldMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFile object")

    def from_file(self, file):
        """
        Copy properties from file object into Dxfile
        :param file: FileMetadata object
        """
        self.__dict__.update(file.__dict__)

    @property
    def cf_meta_name(self):
        return self.field_name

    @property
    def cf_metadata_id(self):
        return self.file_field_metadata_id

    def update(self):
        """
        Update file field data to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.file_field_metadata_id is None):
            print "file_field_metadata_id is required"
            self.__logger.error("file_field_metadata_id is required")
            return 1

        try:
            if self.date_format == '':
                self.date_format = None

            self.__logger.debug("create field input %s" % str(self))
            api_instance = FileFieldMetadataApi(self.__engine.api_client)
            response = api_instance.update_file_field_metadata(self.file_field_metadata_id, self)
            self.__logger.debug("field response %s"
                                % str(response))

            print_message("Field %s updated" % self.field_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
