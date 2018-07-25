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
from dxm.lib.DxTable.DxTable import DxTable
from dxm.lib.DxTable.DxFile import DxFile
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from masking_apis.apis.table_metadata_api import TableMetadataApi
from masking_apis.apis.file_metadata_api import FileMetadataApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

class DxMetaList(object):

    __tableList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxTableList object")

    @classmethod
    def LoadMeta(self, ruleset_id=None):
        """
        Load list of rule sets
        Return None if OK
        """

        notable = None
        nofile = None

        self.__tableList.clear()
        try:
            api_instance = TableMetadataApi(self.__engine.api_client)

            if ruleset_id:
                a = api_instance.get_all_table_metadata(
                        ruleset_id=ruleset_id
                    )
            else:
                a = api_instance.get_all_table_metadata()

            if a.response_list:
                for c in a.response_list:
                    table = DxTable(self.__engine)
                    table.from_table(c)
                    self.__tableList[c.table_metadata_id] = table
            else:
                self.__logger.error("No table metadata found")

        except ApiException as e:
            if (e.status == 404) and (ruleset_id is not None):
                notable = 1
            else:
                print_error(e.body)
                self.__logger.error(e.body)
                return 1


        try:
            api_instance = FileMetadataApi(self.__engine.api_client)

            if ruleset_id:
                a = api_instance.get_all_file_metadata(
                        ruleset_id=ruleset_id
                    )
            else:
                a = api_instance.get_all_file_metadata()

            if a.response_list:
                for c in a.response_list:
                    file = DxFile(self.__engine)
                    file.from_file(c)
                    self.__tableList[c.file_metadata_id] = file
            else:
                self.__logger.error("No file metadata found")

        except ApiException as e:
            if (e.status == 404) and (ruleset_id is not None):
                nofile = 1
            else:
                print_error(e.body)
                self.__logger.error(e.body)
                return 1

        if nofile and notable:
            print_error("Ruleset not found")
            return 1
        else:
            return None

    @classmethod
    def get_by_ref(self, reference):
        """
        return a Table object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__tableList[reference]

        except KeyError as e:
            self.__logger.debug("can't find Table object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__tableList.keys()

    @classmethod
    def get_MetadataId_by_name(self, name, skip_out=None):
        """
        Return metadata id by name.
        :param1 name: name of environment
        :param2 skip_out: disable message printing
        return ref if OK
        return None if ruleset not found or not unique
        """
        reflist = self.get_MetadataId_by_name_worker(name, skip_out, 1)
        # convert list to single value
        # as there will be only one element in list
        if reflist:
            return reflist[0]
        else:
            return None

    @classmethod
    def get_all_MetadataId_by_name(self, name, skip_out=None):
        """
        Return metadata id by name.
        :param1 name: name of environment
        :param2 skip_out: disable message printing
        return list of references if OK
        return None if ruleset not found
        """
        return self.get_MetadataId_by_name_worker(name, skip_out, None)

    @classmethod
    def get_MetadataId_by_name_worker(self, name, skip_out=None,
                                      check_uniqueness=1):
        metalist = get_objref_by_val_and_attribute(name, self, 'meta_name')
        if len(metalist) == 0:
            self.__logger.error('Table or file %s not found' % name)
            if not skip_out:
                print_error('Table or file %s not found' % name)
            return None

        if check_uniqueness:
            if len(metalist) > 1:
                self.__logger.error('Table or file %s is not unique' % name)
                if not skip_out:
                    print_error('Table or file %s is not unique' % name)
                return None

        return metalist

    @classmethod
    def add(self, metaobj):
        """
        Add an Table/File to a list and Engine
        :param metaobj: Table/File object to add to Engine and list
        return None if OK
        """

        if (metaobj.add() is None):
            self.__logger.debug("Adding table/file %s to list" % metaobj)
            self.__tableList[metaobj.meta_id] = metaobj
            return None
        else:
            return 1

    @classmethod
    def delete(self, tableMetadataId):
        """
        Delete a ruleset from a list and Engine
        :param databaseRulesetId: Ruleset id to delete from Engine and list
        return None if OK
        """

        table = self.get_by_ref(tableMetadataId)
        if table is not None:
            if table.delete() is None:
                return None
            else:
                return 1
        else:
            print "Table or File with id %s not found" % tableMetadataId
            return 1

    @classmethod
    def copymeta(self, meta_id, newruleset_id):
        """
        Copy meta data from current RS to new Ruleset
        :param1 meta_id: Metadata id to copy
        :param2 newruleset_id: new RS to copy meta to
        return None if OK
        """
        metaobj = self.get_by_ref(meta_id)
        if type(metaobj) == DxTable:
            newmeta = DxTable(self.__engine)
            newmeta.from_table(metaobj)
            newmeta.ruleset_id = newruleset_id
            if self.add(newmeta):
                return None
            else:
                return newmeta.table_metadata_id
        else:
            newmeta = DxFile(self.__engine)
            newmeta.from_file(metaobj)
            newmeta.ruleset_id = newruleset_id
            if self.add(newmeta):
                return None
            else:
                return newmeta.file_metadata_id
