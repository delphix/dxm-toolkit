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
import sys
from masking_apis.apis.file_format_api import FileFormatApi
from dxm.lib.DxFileFormat.DxFileFormat import DxFileFormat
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error


class DxFileFormatList(object):

    __engine = None
    __filetypeList = {}
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileFormatList object")
        if not self.__filetypeList:
            self.LoadFileFormats()

    @classmethod
    def LoadFileFormats(self):
        """
        Load list of rule sets
        Return None if OK
        """

        try:
            api_instance = FileFormatApi(self.__engine.api_client)

            fileformats = paginator(
                            api_instance,
                            "get_all_file_formats")

            if fileformats.response_list:
                for c in fileformats.response_list:
                    fileformat = DxFileFormat(self.__engine)
                    fileformat.from_filetype(c)
                    self.__filetypeList[c.file_format_id] = fileformat
            else:
                print_error("No file formats found")
                self.__logger.error("No file formats found")

        except ApiException as e:
            print_error("Can't load file formats %s" % e.body)
            return None

    @classmethod
    def get_by_ref(self, reference):
        """
        return a file format object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__filetypeList[reference]

        except KeyError as e:
            self.__logger.debug("can't find file format object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__filetypeList.keys()

    @classmethod
    def get_file_format_id_by_name(self, name):
        reflist = self.get_file_format_id_by_name_worker(name)
        # convert list to single value
        # as there will be only one element in list
        if reflist:
            return reflist[0]
        else:
            return None

    @classmethod
    def get_all_file_format_id_by_name(self, name):
        reflist = self.get_file_format_id_by_name_worker(name)
        return reflist


    @classmethod
    def get_file_format_id_by_name_worker(self, name, check_uniqueness=1):
        """
        :param1 name: name of ruleset
        :param2 check_uniqueness: check uniqueness put None if skip this check
        return list of rulesets
        """
        reflist = get_objref_by_val_and_attribute(name, self, 'file_format_name')
        if len(reflist) == 0:
            self.__logger.error('File format %s not found' % name)
            print_error('File format %s not found' % name)
            return None

        if check_uniqueness:
            if len(reflist) > 1:
                self.__logger.error('File format %s is not unique' % name)
                print_error('File format %s is not unique' % name)
                return None

        return reflist


    @classmethod
    def get_all_file_format_id_by_type(self, name):
        reflist = self.get_file_format_id_by_type_worker(name, 0)
        return reflist


    @classmethod
    def get_file_format_id_by_type_worker(self, name, check_uniqueness=1):
        """
        :param1 name: name of ruleset
        :param2 check_uniqueness: check uniqueness put None if skip this check
        return list of rulesets
        """
        reflist = get_objref_by_val_and_attribute(name, self, 'file_format_type')
        if len(reflist) == 0:
            self.__logger.error('File format %s not found' % name)
            print_error('File format %s not found' % name)
            return None

        if check_uniqueness:
            if len(reflist) > 1:
                self.__logger.error('File format %s is not unique' % name)
                print_error('File format %s is not unique' % name)
                return None

        return reflist

    @classmethod
    def add(self, filetype):
        """
        Add an File type to a list and Engine
        :param ruleset: File type object to add to Engine and list
        return None if OK
        """

        if (filetype.add() == 0):
            self.__logger.debug("Adding file type %s to list" % filetype)
            self.__filetypeList[filetype.file_format_id] = filetype
            return None
        else:
            return 1

    @classmethod
    def delete(self, filetype_ref):
        """
        Add an File type to a list and Engine
        :param filetype_ref: File format ref to delete from engine and list
        return None if OK
        """

        fileformat = self.get_by_ref(filetype_ref)
        if fileformat is not None:
            if fileformat.delete() is None:
                return None
            else:
                return 1
        else:
            print_error("File format type with id %s not found" % filetype_ref)
            return 1
