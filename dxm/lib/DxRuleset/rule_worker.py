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
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxTable.DxMetaList import DxMetaList


def ruleset_listmeta(p_engine, format, rulesetname, envname, metaname):
    """
    List tables/file from ruleset
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: rulesetname: ruleset name to display metadata from
    param4: envname: environemnt name to display metadata from
    param5: metamame: name of table/file to display
    return 0 if added, non zero for error
    """

    ret = 0
    found = False

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Environent name", 30),
                    ("Ruleset name", 30),
                    ("Metadata type", 15),
                    ("Metadata name", 32)
                  ]
    data.create_header(data_header)
    data.format_type = format
    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)
        connlist = DxConnectorsList()
        connlist.LoadConnectors(envname)

        if rulesetname:
            rulesetref_list = rulelist.get_all_rulesetId_by_name(rulesetname)
            if rulesetref_list is None:
                ret = ret + 1
                continue
        else:
            rulesetref_list = rulelist.get_allref()
            if rulesetref_list is None:
                continue

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
                data.data_insert(
                                  engine_tuple[0],
                                  environment_name,
                                  ruleobj.ruleset_name,
                                  ruleobj.type,
                                  metaobj.meta_name
                                )

    print("")
    print (data.data_output(False))
    print("")

    if found:
        return 0
    else:
        if metaname:
            print_error("Table or file %s not found" % metaname)
        return ret

def ruleset_addmeta(p_engine, params, inputfile):
    """
    Add matadata to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: set of required parameters to add meta
    param3: inputfile: file with table/file definition
    return 0 if added, non 0 for error
    """

    ret = 0

    rulesetname = params["rulesetname"]
    envname = params["envname"]

    enginelist = get_list_of_engines(p_engine)

    if (params["metaname"] is None) and (inputfile is None):
        print_error("Option metaname or inputfile is required")
        return 1

    if (params["metaname"]) and (inputfile):
        print_error("Option metaname and inputfile are mutally exclusive")
        return 1

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)
        ruleref = rulelist.get_rulesetId_by_name(rulesetname)

        if ruleref:
            ruleobj = rulelist.get_by_ref(ruleref)
            if (params["metaname"]):
                ret = ret + ruleobj.addmeta(params)
            else:
                ret = ret + ruleobj.addmetafromfile(inputfile)
        else:
            ret = ret + 1

    return ret


def ruleset_deletemeta(p_engine, rulesetname, metaname, envname):
    """
    Delete meta (file, table) from ruleset to Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: metaname: metaname to delete
    param4: envname: environment name
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)
        ruleref = rulelist.get_rulesetId_by_name(rulesetname)

        metalist = DxMetaList()
        metalist.LoadMeta(ruleset_id=ruleref)

        metaref = metalist.get_MetadataId_by_name(metaname)

        if metaref:
            if metalist.delete(metaref):
                ret = ret + 1
        else:
            ret = ret + 1

    return ret


def ruleset_add(p_engine, rulesetname, connectorname, envname):
    """
    Add ruleset to Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: connectorname: connectorname name
    param4: envname: environment name
    return 0 if added, non 0 for error
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        connlist = DxConnectorsList()
        connlist.LoadConnectors(envname)
        logger.debug("Connector is %s" % connectorname)
        connref = connlist.get_connectorId_by_name(connectorname)
        connobj = connlist.get_by_ref(connref)
        if connobj.is_database:
            ruleset = DxDatabaseRuleset(engine_obj)
            ruleset.ruleset_name = rulesetname
            ruleset.database_connector_id = connref
        else:
            ruleset = DxFileRuleset(engine_obj)
            ruleset.ruleset_name = rulesetname
            ruleset.file_connector_id = connref

        if rulelist.add(ruleset):
            ret = ret + 1

    return ret


def ruleset_delete(p_engine, rulesetname, envname):
    """
    Delete ruleset from Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    return 0 if added, non 0 for error
    """
    return ruleset_worker(p_engine=p_engine, rulesetname=rulesetname,
                          envname=envname, function_to_call='do_delete')

def ruleset_clone(p_engine, rulesetname, envname, newname):
    """
    Delete ruleset from Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: envname: environment name
    param4: newname: new ruleset name
    return 0 if added, non 0 for error
    """
    return ruleset_worker(p_engine=p_engine, rulesetname=rulesetname,
                          envname=envname, function_to_call='do_clone',
                          newname=newname)

def ruleset_worker(**kwargs):
    """
    Delete ruleset from Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: function_to_call: function to call for particual ruleset
    return 0 if added, non 0 for error
    """

    p_engine = kwargs.get('p_engine')
    rulesetname = kwargs.get('rulesetname')
    envname = kwargs.get('envname')
    function_to_call = kwargs.get('function_to_call')

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])
        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)
        ruleref = rulelist.get_rulesetId_by_name(rulesetname)
        if ruleref:
            dynfunc = globals()[function_to_call]
            if dynfunc(ruleref=ruleref, rulelist=rulelist,
                       engine_obj=engine_obj, **kwargs):
                ret = ret + 1
        else:
            ret = ret + 1

    return ret


def do_delete(**kwargs):
    rulelist = kwargs.get('rulelist')
    ruleref = kwargs.get('ruleref')
    return rulelist.delete(ruleref)

def do_clone(**kwargs):
    rulelist = kwargs.get('rulelist')
    ruleref = kwargs.get('ruleref')
    newname = kwargs.get('newname')
    newref = rulelist.copy(ruleref, newname)

    if newref is None:
        return 1

    if do_meta_copy(kwargs.get('engine_obj'), ruleref, newref) != 0:
        return 1

    return None


def do_meta_copy(engine_obj, ruleref, newref):
    """
    Copy a meta objects plus columns from one RS to new one
    param1: p_engine: engine name from configuration
    param2: ruleref: source ruleset
    param3: newref: target ruleset
    return 0 if no issue with copy
    """
    ret = 0
    metalist = DxMetaList()
    metalist.LoadMeta(ruleref)

    for meta_id in metalist.get_allref():
        newmeta_id = metalist.copymeta(meta_id, newref)
        if newmeta_id:
            ret = ret + columns_copy(engine_obj, meta_id, newmeta_id)
        else:
            ret = ret + 1

    return ret


def ruleset_list(p_engine, format, rulesetName, envname):
    """
    Print list of ruleset by ruleset name or environment name
    param1: p_engine: engine name from configuration
    param2: format: output format
    param2: ruleset: name of ruleset to display
    param3: envname: name of environment to list ruleset
    return 0 if environment found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Ruleset name", 30),
                    ("Connector name", 30),
                    ("Metadata type", 15),
                    ("Connector type", 15),
                    ("Environent name", 30)
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])
        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)

        if rulesetName is None:
            rulesets = rulelist.get_allref()
            if len(rulesets) == 0:
                ret = ret + 1
                continue
        else:
            rulesets = rulelist.get_all_rulesetId_by_name(rulesetName)
            if rulesets is None:
                ret = ret + 1
                continue

        connlist = DxConnectorsList()
        connlist.LoadConnectors(envname)

        for ruleid in rulesets:
            ruleobj = rulelist.get_by_ref(ruleid)
            connobj = connlist.get_by_ref(ruleobj.connectorId)

            if connobj:
                envobj = envlist.get_by_ref(connobj.environment_id)
                connector_name = connobj.connector_name
                environment_name = envobj.environment_name
                connector_type = connobj.connector_type
            else:
                connector_name = 'N/A'
                environment_name = 'N/A'
                connector_type = 'N/A'

            data.data_insert(
                              engine_tuple[0],
                              ruleobj.ruleset_name,
                              connector_name,
                              ruleobj.type,
                              connector_type,
                              environment_name
                            )

    print("")
    print (data.data_output(False))
    print("")
    return ret
