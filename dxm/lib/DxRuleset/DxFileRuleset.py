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
import csv

from dxm.lib.DxTable.DxFile import DxFile
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList
from dxm.lib.DxRuleset.DxDatabaseRuleset import DxDatabaseRuleset
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.file_ruleset_api import FileRulesetApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel

class DxFileRuleset(object):

    swagger_types = {
        'file_ruleset_id': 'int',
        'ruleset_name': 'str',
        'file_connector_id': 'int'
    }

    swagger_map = {
        'file_ruleset_id': 'fileRulesetId',
        'ruleset_name': 'rulesetName',
        'file_connector_id': 'fileConnectorId'
    }

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #FileRuleset.__init__(self)
        self.__engine = engine
        self.__fileList = None
        self.__type = 'File'
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileRuleset object")

        self.__api = FileRulesetApi
        self.__apiexc = ApiException
        self.__obj = None

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def logger(self):
        return self.__logger

    @property
    def engine(self):
        return self.__engine


    @property
    def type(self):
        return self.__type

    @property
    def ruleset_id(self):
        return self.obj.file_ruleset_id

    @property
    def ruleset_name(self):
        return self.obj.ruleset_name

    @property
    def connectorId(self):
        return 'f' + str(self.obj.file_connector_id)

    @property
    def file_connector_id(self):
        return self.obj.file_connector_id

    @file_connector_id.setter
    def file_connector_id(self, file_connector_id):
        self.obj.file_connector_id = file_connector_id

    def from_ruleset(self, ruleset):
        """
        Set obj object with real ruleset object
        :param con: DatabaseConnector object
        """
        self.__obj = ruleset
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map

    def create_file_ruleset(self, ruleset_name, file_connector_id):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  
        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.ruleset_name = ruleset_name
        self.obj.file_connector_id = file_connector_id


    def add(self):
        """
        Add ruleset to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.ruleset_name is None):
            print_error("Ruleset name is required")
            self.__logger.error("Ruleset name is required")
            return 1

        if (self.obj.file_connector_id is None):
            print_error("File connector Id is required")
            self.__logger.error("File connector ID is required")
            return 1

        try:
            self.__logger.debug("create database ruleset input %s" % str(self))

            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_file_ruleset(self.obj)
            self.__obj = response

            self.__logger.debug("ruleset response %s"
                                % str(response))

            print_message("Ruleset %s added" % self.ruleset_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete ruleset from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete ruleset id %s"
                                % self.ruleset_id)
            response = api_instance.delete_file_ruleset(
                        self.ruleset_id
                       )
            self.__logger.debug("delete ruleset response %s"
                                % str(response))
            print_message("Ruleset %s deleted" % self.ruleset_name)
            return None
        except self.__apiexc as e:
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
        #connlist.LoadConnectors(None)

        connobj = connlist.get_by_ref(self.connectorId)

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

        if enclosure:
            enclosure = enclosure.strip()

        file = DxFile(self.__engine)
        file.create_file(
            file_name = filename,
            ruleset_id = self.ruleset_id,
            file_type = connobj.connector_type,
            file_format_id = file_format,
            delimiter = delimiter,
            end_of_record = eor_string,
            enclosure = enclosure,
            name_is_regular_expression=regular
        )
        return file.add()

    def skip_comment(self, file):
        for line in file:
            if line.startswith('#'):
                continue
            if line:
                yield line

    def addmetafromfile(self, inputfile):
        """
        Add file from file to ruleset
        :param inputfile: file with files definition
        return a 0 if non error
        return 1 in case of error
        """
        ret = 0
        for columns in csv.reader(
                    self.skip_comment(inputfile),
                    quotechar='"',
                    delimiter=',',
                    escapechar='\\',
                    skipinitialspace=True):

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

    def addmetafromfetch(self, fetchfilter, bulk):
        """
        Add tables from fetch into ruleset
        :param fetchfilter: filter for tables
        return a 0 if non error
        return 1 in case of error
        """
        
        connobj = DxConnectorsList.get_by_ref(self.connectorId)
        table_list = []
        ret = 0

        if bulk:
            print_error("Bulk option is not supported for files")
            return 1

        if fetchfilter:
            fetchfilter = re.escape(fetchfilter).replace("\*",".*")
            self.logger.debug("fetchfilter {}".format(fetchfilter))
            pattern = re.compile(r'^{}$'.format(fetchfilter))

        for table in connobj.fetch_meta():
            params = {
                "metaname": table,
                "file_name_regex": None,
                "file_format": None,
                "file_delimiter": None,
                "file_eor": None,
                "file_enclosure": None
            }

            self.logger.debug("checking file {}".format(table))

            if fetchfilter:
                if pattern.search(table):
                    self.logger.debug("filtered file added to bulk{}".format(table))
                    ret = ret + self.addmeta(params)
            else:
                    if bulk:
                        table_list.append(params)
                    else:
                        ret = ret + self.addmeta(params)            
        
        return ret


    def refresh(self):
        """
        Refresh ruleset on the Masking engine 
        return a None if non error
        return 1 in case of error
        """
        print_error("Refresh operation is not supported for files")
        return 1
