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
from masking_apis.models.file_ruleset import FileRuleset
from masking_apis.apis.file_ruleset_api import FileRulesetApi
from dxm.lib.DxTable.DxFile import DxFile
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

class DxFileRuleset(FileRuleset):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        FileRuleset.__init__(self)
        self.__engine = engine
        self.__fileList = None
        self.__type = 'File'
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileRuleset object")

    @property
    def type(self):
        return self.__type

    @property
    def ruleset_id(self):
        return self.file_ruleset_id

    @property
    def connectorId(self):
        return self.file_connector_id

    def from_ruleset(self, ruleset):
        """
        Copy properties from Ruleset object into DxRuleset
        :param con: DatabaseConnector object
        """
        self.__dict__.update(ruleset.__dict__)

    def add(self):
        """
        Add ruleset to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.ruleset_name is None):
            print "Ruleset name is required"
            self.__logger.error("Ruleset name is required")
            return 1

        if (self.file_connector_id is None):
            print "File connector Id is required"
            self.__logger.error("File connector ID is required")
            return 1

        try:
            self.__logger.debug("create database ruleset input %s" % str(self))

            api_instance = FileRulesetApi(self.__engine.api_client)
            response = api_instance.create_file_ruleset(self)
            self.file_ruleset_id = response.file_ruleset_id

            self.__logger.debug("ruleset response %s"
                                % str(response))

            print_message("Ruleset %s added" % self.ruleset_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete ruleset from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = FileRulesetApi(self.__engine.api_client)

        try:
            self.__logger.debug("delete ruleset id %s"
                                % self.rulesetId)
            response = api_instance.delete_file_ruleset(
                        self.rulesetId
                       )
            self.__logger.debug("delete ruleset response %s"
                                % str(response))
            print_message("Ruleset %s deleted" % self.ruleset_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def addmeta(self, file_params):
        """
        Add file to ruleset
        :param file_params: set of file parametes
        return a None if non error
        return 1 in case of error
        """

        filename = file_params["metaname"]
        file_format = file_params["file_format"]
        regular = file_params["file_name_regex"]
        delimiter = file_params["file_delimiter"]
        eor = file_params["file_eor"]
        enclosure = file_params["file_enclosure"]

        connlist = DxConnectorsList()
        connlist.LoadConnectors(None)
        connobj = connlist.get_by_ref(self.file_connector_id)

        if filename is None:
            print_error("File name is required")
            self.__logger.error("File name is required")
            return 1

        if eor == 'custom':
            if file_params["file_eor_custom"]:
                eor_string = file_params["file_eor_custom"]
            else:
                print_error("Custom End of record is unknown")
                self.__logger.error("Custom End of record is unknown")
                return 1
        else:
            eor_string = eor

        file = DxFile(self.__engine)
        file.file_name = filename
        file.ruleset_id = self.file_ruleset_id
        file.file_type = connobj.file_type
        file.file_format_id = file_format
        file.name_is_regular_expression = regular
        file.delimiter = delimiter
        file.end_of_record = eor_string
        file.enclosure = enclosure

        return file.add()

    def addmetafromfile(self, inputfile):
        """
        Add file from file to ruleset
        :param inputfile: file with files definition
        return a 0 if non error
        return 1 in case of error
        """
        ret = 0
        for line in inputfile:
            if line.startswith('#'):
                continue
            columns = line.strip().split(',')
            params = {
                "metaname": columns[0],
                "file_name_regex": columns[1],
                "file_format": columns[2],
                "file_delimiter": columns[3],
                "file_eor": columns[4],
                "file_enclosure": columns[5]
            }
            ret = ret + self.addmeta(params)

        return ret
