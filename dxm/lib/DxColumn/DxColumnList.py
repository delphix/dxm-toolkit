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
from dxm.lib.DxColumn.DxDBColumn import DxDBColumn
from dxm.lib.DxColumn.DxFileField import DxFileField
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTable.DxMetaList import DxMetaList
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

from dxm.lib.masking_api.api.column_metadata_api import ColumnMetadataApi
from dxm.lib.masking_api.api.file_field_metadata_api import FileFieldMetadataApi
from dxm.lib.masking_api.rest import ApiException

class DxColumnList(object):

    def __init__(self):
        """
        Constructor
        """
        self.__engine = DxMaskingEngine
        self.__columnList = {}
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxColumnList object")

    def LoadColumns(self, metadata_id=None, is_masked=None):
        """
        Load list of column metadata
        Return None if OK
        """

        notable = None
        nofile = None

        metaobj = DxMetaList.get_by_ref(metadata_id)

        self.__api = ColumnMetadataApi
        self.__fileapi = FileFieldMetadataApi
        self.__apiexc = ApiException


        if ((metadata_id is None) or (type(metaobj) == DxTable)):
            try:
                api_instance = self.__api(self.__engine.api_client)

                if is_masked:
                    if metadata_id:
                        columns = paginator(
                                api_instance,
                                "get_all_column_metadata",
                                table_metadata_id=metadata_id,
                                is_masked=is_masked)
                    else:
                        columns = paginator(
                                api_instance,
                                "get_all_column_metadata",
                                is_masked=is_masked)
                else:
                    if metadata_id:
                        columns = paginator(
                                api_instance,
                                "get_all_column_metadata",
                                table_metadata_id=metadata_id)
                    else:
                        columns = paginator(
                                api_instance,
                                "get_all_column_metadata")

                if columns.response_list:
                    for c in columns.response_list:
                        column = DxDBColumn(self.__engine, existing_object=c)
                        self.__columnList[column.cf_metadata_id] = column
                else:
                    # print_error("No column metadata found")
                    self.__logger.error("No column metadata found")

            except self.__apiexc as e:
                if (e.status == 404) and (metadata_id is not None):
                    notable = 1
                else:
                    print_error(e.body)
                    self.__logger.error(e.body)
                    return 1

        elif ((metadata_id is None) or (type(metaobj) == DxFile)):
            try:
                api_instance = self.__fileapi(self.__engine.api_client)

                if metadata_id and (metaobj.file_format_id is None):
                    # File doesn't have a file type set so there is no masking
                    return None

                if is_masked:
                    if metadata_id:
                        fields = paginator(
                                api_instance,
                                "get_all_file_field_metadata",
                                file_format_id=metaobj.file_format_id,
                                is_masked=is_masked)
                    else:
                        fields = paginator(
                                api_instance,
                                "get_all_file_field_metadata",
                                is_masked=is_masked)
                else:
                    if metadata_id:
                        fields = paginator(
                                api_instance,
                                "get_all_file_field_metadata",
                                file_format_id=metaobj.file_format_id)
                    else:
                        fields = paginator(
                                api_instance,
                                "get_all_file_field_metadata")

                if fields.response_list:
                    for c in fields.response_list:
                        column = DxFileField(self.__engine, existing_object=c)
                        self.__columnList[column.cf_metadata_id] = column
                else:
                    print_error("No field metadata found")
                    self.__logger.error("No field metadata found")

            except self.__apiexc as e:
                if (e.status == 404) and (metadata_id is not None):
                    nofile = 1
                else:
                    print_error(e.body)
                    self.__logger.error(e.body)
                    return 1

        if nofile and notable:
            print_error("Columns for meta id not found")
            return 1
        else:
            return None

    def get_by_ref(self, reference):
        """
        return a Table object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__columnList[reference]

        except KeyError as e:
            self.__logger.debug("can't find Table object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)


    def get_allref(self, sortby1='cf_meta_name'):
        """
        return a list of all references
        """

        return sorted(self.__columnList, key=lambda k:
                      getattr(self.__columnList[k], sortby1).lower())

    def get_column_id_by_algorithm(self, alg):
        return get_objref_by_val_and_attribute(alg, self, 'algorithm_name')

    def get_column_id_by_name(self, name):
        reflist = get_objref_by_val_and_attribute(name, self, 'cf_meta_name')
        if len(reflist) == 0:
            self.__logger.error('Column name %s not found' % name)
            print_error('Column name %s not found' % name)
            return None

        if len(reflist) > 1:
            self.__logger.error('Column name %s is not unique' % name)
            print_error('Column name %s is not unique' % name)
            return None

        return reflist[0]


    # def add(self, table):
    #     """
    #     Add an Table to a list and Engine
    #     :param table: Table object to add to Engine and list
    #     return None if OK
    #     """
    #
    #     if (table.add() is None):
    #         self.__logger.debug("Adding table %s to list" % table)
    #         self.__tableList[table.tableMetadataId] = table
    #         return None
    #     else:
    #         return 1
    #
    #
    # def delete(self, tableMetadataId):
    #     """
    #     Delete a ruleset from a list and Engine
    #     :param databaseRulesetId: Ruleset id to delete from Engine and list
    #     return None if OK
    #     """
    #
    #     table = self.get_by_ref(tableMetadataId)
    #     if table is not None:
    #         if table.delete() is None:
    #             return None
    #         else:
    #             return 1
    #     else:
    #         print "Table or File with id %s not found" % tableMetadataId
    #         return 1
