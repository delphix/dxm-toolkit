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
# Date    : July 2018


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines
from dxm.lib.DxColumn.column_worker import columns_copy
from dxm.lib.DxRuleset.DxDatabaseRuleset import DxDatabaseRuleset
from dxm.lib.DxRuleset.DxFileRuleset import DxFileRuleset
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxTable.DxMetaList import DxMetaList


def tab_listtable_details(p_engine, p_username,  p_format, rulesetname, envname, metaname):
    """
    List details of tables/file from ruleset
    param1: p_engine: engine name from configuration
    param2: p_format: output format
    param3: rulesetname: ruleset name to display metadata from
    param4: envname: environemnt name to display metadata from
    param5: metamame: name of table/file to display
    return 0 if added, non zero for error
    """
    return tab_list_details(
        p_engine,
        p_format,
        rulesetname,
        envname,
        metaname,
        'Database')

def tab_listfile_details(p_engine, p_username,  p_format, rulesetname, envname, metaname):
    """
    List details of tables/file from ruleset
    param1: p_engine: engine name from configuration
    param2: p_format: output format
    param3: rulesetname: ruleset name to display metadata from
    param4: envname: environemnt name to display metadata from
    param5: metamame: name of table/file to display
    return 0 if added, non zero for error
    """
    return tab_list_details(
        p_engine,
        p_format,
        rulesetname,
        envname,
        metaname,
        'File')

def tab_list_details(p_engine, p_username,  p_format, rulesetname, envname, metaname, what):
    """
    List details of tables/file from ruleset
    param1: p_engine: engine name from configuration
    param2: p_format: output format
    param3: rulesetname: ruleset name to display metadata from
    param4: envname: environemnt name to display metadata from
    param5: metamame: name of table/file to display
    param6: what - Database/File
    return 0 if added, non zero for error
    """

    ret = 0
    found = False

    data = DataFormatter()

    if what == 'Database':
        data_header = [
                        ("Engine name", 30),
                        ("Environent name", 30),
                        ("Ruleset name", 30),
                        ("Table name", 32),
                        ("Logical key", 32),
                        ("Where clause", 50),
                        ("Custom SQL", 50)
                      ]
    else:
        data_header = [
                        ("Engine name", 30),
                        ("Environent name", 30),
                        ("Ruleset name", 30),
                        ("File name", 32),
                        ("File type", 32),
                        ("File format name", 32),
                        ("Delimiter", 10),
                        ("End of record", 10)
                      ]

    data.create_header(data_header)

    data.format_type = p_format

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList(envname)
        #rulelist.LoadRulesets()
        connlist = DxConnectorsList(envname)
        #connlist.LoadConnectors()

        if rulesetname:
            rulesetref_all = rulelist.get_all_rulesetId_by_name(rulesetname)
            if rulesetref_all is None:
                ret = ret + 1
                continue
            rulesetref_list = [x for x in rulesetref_all
                               if rulelist.get_by_ref(x).type == what]
            if rulesetref_list is None:
                ret = ret + 1
                continue
        else:
            if what == 'Database':
                rulesetref_list = rulelist.get_all_database_rulesetIds()
                if rulesetref_list is None:
                    continue
            else:
                rulesetref_list = rulelist.get_all_file_rulesetIds()
                if rulesetref_list is None:
                    continue

        filetypelist = DxFileFormatList()
        metalist = DxMetaList()

        for ruleref in rulesetref_list:
            ruleobj = rulelist.get_by_ref(ruleref)
            connobj = connlist.get_by_ref(ruleobj.connectorId)
            if connobj:
                envobj = envlist.get_by_ref(connobj.environment_id)
                environment_name = envobj.environment_name
            else:
                environment_name = 'N/A'

            metalist.LoadMeta(ruleobj.ruleset_id)

            if metaname:
                metalist_ref = metalist.get_all_MetadataId_by_name(metaname, 1)
                if metalist_ref is None:
                    ret = ret + 1
                    continue
                found = True
            else:
                metalist_ref = metalist.get_allref()
                if metalist_ref is None:
                    continue

            for metaid in metalist_ref:
                metaobj = metalist.get_by_ref(metaid)
                if what == 'Database':
                    data.data_insert(
                                      engine_tuple[0],
                                      environment_name,
                                      ruleobj.ruleset_name,
                                      metaobj.meta_name,
                                      metaobj.key_column,
                                      repr(metaobj.where_clause),
                                      repr(metaobj.custom_sql)
                                    )
                else:
                    if metaobj.file_format_id is not None:
                        fileformatobj = filetypelist.get_by_ref(
                            metaobj.file_format_id)
                        fileformatname = fileformatobj.file_format_name
                    else:
                        fileformatname = 'N/A'

                    data.data_insert(
                                      engine_tuple[0],
                                      environment_name,
                                      ruleobj.ruleset_name,
                                      metaobj.meta_name,
                                      metaobj.file_type,
                                      fileformatname,
                                      metaobj.delimiter,
                                      repr(metaobj.end_of_record)
                                    )

    print("")
    print (data.data_output(False))
    print("")

    if found:
        return 0
    else:
        if metaname:
            print_error("Table %s not found" % metaname)
        return ret

def tab_update_meta(p_engine, p_username,  params):
    rulesetname = params["rulesetname"]
    metaname = params["metaname"]
    envname = params["envname"]
    return tab_selector(p_engine, p_username,  rulesetname, envname, metaname, None, params)


def tab_selector(p_engine, p_username,  rulesetname, envname, metaname, function_to_call,
                 params):
    """
    List details of tables/file from ruleset
    param1: p_engine: engine name from configuration
    param2: p_format: output format
    param3: rulesetname: ruleset name to display metadata from
    param4: envname: environemnt name to display metadata from
    param5: metamame: name of table/file to display
    param6: what - Database/File
    return 0 if added, non zero for error
    """

    ret = 0
    update = False

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList(envname)
        #rulelist.LoadRulesets()
        if rulesetname:
            ruleref = rulelist.get_rulesetId_by_name(rulesetname)
        else:
            ruleref = None

        metalist = DxMetaList()
        metalist.LoadMeta(ruleset_id=ruleref)

        metaref = metalist.get_MetadataId_by_name(metaname)

        if metaref:
            metaobj = metalist.get_by_ref(metaref)
        else:
            ret = ret + 1
            continue

        param_map = {
            "custom_sql": "custom_sql",
            "where_clause": "where_clause",
            "having_clause": "having_clause",
            "key_column": "key_column",
            "file_format": "file_format_id",
            "file_delimiter": "delimiter",
            "file_eor": "end_of_record",
            "file_enclosure": "enclosure",
            "file_name_regex": "name_is_regular_expression"
        }

        eor = params["file_eor"]
        if eor == 'custom':
            if params["file_eor_custom"]:
                params["file_eor"] = params["file_eor_custom"]
            else:
                print_error("Custom End of record is unknown")
                return 1

        for p in param_map.keys():
            if params[p] or params[p]=='':
                if param_map[p] in metaobj.obj.swagger_map:
                    update = True
                    value = params[p]
                    if value == '':
                        value = None
                    setattr(metaobj.obj, param_map[p], value)

        if update:
            ret = ret + metaobj.update()

    return ret
