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
import json
from operator import xor
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
from dxm.lib.DxColumn.column_worker import column_export
from dxm.lib.DxColumn.column_worker import column_setmasking
from dxm.lib.DxColumn.column_worker import column_unsetmasking
from dxm.lib.DxColumn.column_worker import column_check
from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList


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
        engine_obj = DxMaskingEngine(engine_tuple)

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


def ruleset_addmeta(p_engine, params, inputfile, fromconnector, bulk):
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

    if (params["metaname"] is None) and (inputfile is None) and (fromconnector is None):
        print_error("Option metaname, inputfile or fromconnector is required")
        return 1

    if ((params["metaname"]) and inputfile) or \
       ((params["metaname"]) and fromconnector) or \
       (inputfile and fromconnector):
        print_error("Option metaname, fromconnector and inputfile are mutally exclusive")
        return 1

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

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
            elif inputfile:
                ret = ret + ruleobj.addmetafromfile(inputfile, bulk)
            elif fromconnector:
                ret = ret + ruleobj.addmetafromfetch(params["fetchfilter"], bulk)
            else:
                print_error("Source for add meta is not specified")
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
        engine_obj = DxMaskingEngine(engine_tuple)

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
        engine_obj = DxMaskingEngine(engine_tuple)

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
        if connobj:
            if connobj.is_database:
                ruleset = DxDatabaseRuleset(engine_obj)
                ruleset.create_database_ruleset(
                    ruleset_name = rulesetname,
                    database_connector_id=connobj.connectorId,
                    refresh_drops_tables=None)
            else:
                ruleset = DxFileRuleset(engine_obj)
                ruleset.create_file_ruleset(
                    ruleset_name = rulesetname,
                    file_connector_id =connobj.connectorId)

            if rulelist.add(ruleset):
                ret = ret + 1
        else:
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


def ruleset_refresh(p_engine, rulesetname, envname):
    """
    Refresh ruleset on the Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: envname: environment name
    return 0 if added, non 0 for error
    """
    return ruleset_worker(p_engine=p_engine, rulesetname=rulesetname,
                          envname=envname, function_to_call='do_refresh')

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
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        # envlist = DxEnvironmentList()
        # envlist.LoadEnvironments()
        # rulelist = DxRulesetList()
        rulelist = DxRulesetList(envname)
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


def do_refresh(**kwargs):
    rulelist = kwargs.get('rulelist')
    ruleref = kwargs.get('ruleref')
    return rulelist.refresh(ruleref)

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

    ret = ruleset_list_worker(
            p_engine=p_engine,
            format=format,
            rulesetName=rulesetName,
            envname=envname,
            function_to_call="do_list",
            data=data)

    print("")
    print (data.data_output(False))
    print("")
    return ret


def ruleset_list_worker(**kwargs):
    """
    Print list of ruleset by ruleset name or environment name
    param1: p_engine: engine name from configuration
    param2: format: output format
    param2: ruleset: name of ruleset to display
    param3: envname: name of environment to list ruleset
    return 0 if environment found
    """

    p_engine = kwargs.get('p_engine')
    format = kwargs.get('format')
    rulesetName = kwargs.get('rulesetName')
    envname = kwargs.get('envname')
    function_to_call = kwargs.get('function_to_call')
    data = kwargs.get('data')

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        #envlist = DxEnvironmentList()
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

        # connlist = DxConnectorsList(envname)
        # connlist.LoadConnectors(envname)

        for ruleid in rulesets:
            ruleobj = rulelist.get_by_ref(ruleid)
            connobj = DxConnectorsList.get_by_ref(ruleobj.connectorId)

            dynfunc = globals()[function_to_call]
            if dynfunc(ruleobj=ruleobj, connobj=connobj,
                       # envlist=envlist,
                       engine_obj=engine_obj, **kwargs):
                ret = ret + 1
                continue

    return ret

def do_list(**kwargs):

    engine_obj = kwargs.get('engine_obj')
    connobj = kwargs.get('connobj')
    ruleobj = kwargs.get('ruleobj')
    envlist = DxEnvironmentList
    data = kwargs.get('data')

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
                      engine_obj.get_name(),
                      ruleobj.ruleset_name,
                      connector_name,
                      ruleobj.type,
                      connector_type,
                      environment_name
                    )
    return 0

# export / import functionality


def ruleset_export(p_engine, rulesetname, envname, outputfile,
                   exportmeta, metaname):
    """
    Delete ruleset from Masking engine
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: envname: environment name
    param4: exportmeta: export metadata with ruleset
    param5: metaname: limit export to single meta object
    return 0 if added, non 0 for error
    """

    exp = []

    ret = ruleset_worker(
            p_engine=p_engine,
            rulesetname=rulesetname,
            envname=envname,
            function_to_call="do_export",
            exportout=exp,
            exportmeta=exportmeta,
            metaname=metaname)

    if ret == 0:
        try:
            json.dump(exp, outputfile, indent=4)
            outputfile.close()
            print_message("Ruleset exported to file %s" % outputfile.name)
            return 0
        except Exception as e:
            print_error("Problem with file %s Error: %s" %
                        (outputfile.name, str(e)))
            return 1

    else:
        return 1


def do_export(**kwargs):
    """
    Export ruleset into external object
    """

    ruleref = kwargs.get('ruleref')
    rulelist = kwargs.get('rulelist')
    exportout = kwargs.get('exportout')
    exportmeta = kwargs.get('exportmeta')
    metaname = kwargs.get('metaname')
    engine_obj = kwargs.get('engine_obj')
    envlist = DxEnvironmentList

    ruleobj = rulelist.get_by_ref(ruleref)
    connobj = DxConnectorsList.get_by_ref(ruleobj.connectorId)

    logger = logging.getLogger()

    ret = 0

    if connobj:
        envobj = envlist.get_by_ref(connobj.environment_id)
        connector_name = connobj.connector_name
        environment_name = envobj.environment_name
    else:
        connector_name = 'N/A'
        environment_name = None

    ruleset = {
        "Ruleset name": ruleobj.ruleset_name,
        "Connector name": connector_name,
        "Environent name": environment_name}

    if exportmeta == 'Y':
        metadatalist = []
        metalist = DxMetaList()
        metalist.LoadMeta(ruleobj.ruleset_id)

        if metaname:
            metalist_ref = metalist.get_all_MetadataId_by_name(metaname, 1)
            if metalist_ref is None:
                logger.error("no meta %s found" % metaname)
                return 1
        else:
            metalist_ref = metalist.get_allref()
            if metalist_ref is None:
                logger.error("no meta data found")
                return 1

        for metaid in metalist_ref:
            metaobj = metalist.get_by_ref(metaid)

            if connobj.is_database:
                tabhash = {
                  "table": True,
                  "meta_name": metaobj.meta_name,
                  "key_column": metaobj.key_column,
                  "where_clause": repr(metaobj.where_clause),
                  "custom_sql": repr(metaobj.custom_sql)
                }
            else:
                if metaobj.file_format_id is not None:
                    filetypelist = DxFileFormatList()
                    fileformatobj = filetypelist.get_by_ref(
                        metaobj.file_format_id)
                    fileformatname = fileformatobj.file_format_name
                else:
                    fileformatname = 'N/A'

                tabhash = {
                  "table": False,
                  "meta_name": metaobj.meta_name,
                  "file_format": fileformatname,
                  "file_delimiter": metaobj.delimiter,
                  "file_eor": metaobj.end_of_record,
                  "file_enclosure": metaobj.enclosure,
                  "file_name_regex": metaobj.name_is_regular_expression
                }

            metadatalist.append(tabhash)

        ruleset["Metadata"] = metadatalist
        columndata = column_export(
                        engine_obj.get_name(), None, ruleobj.ruleset_name,
                        environment_name, metaname, None, None)
        ruleset["Columns"] = json.loads(columndata.data_output(False))
    else:
        ruleset["Metadata"] = []
        ruleset["Columns"] = []

    exportout.append(ruleset)
    return ret


def ruleset_import(p_engine, inputfile, rulesetname, connectorname, envname):
    rulesets = json.load(inputfile)
    # if it's one allow override of values

    ret = 0

    for ruleset in rulesets:

        if len(rulesets) < 2:
            if rulesetname:
                runrulesetname = rulesetname
            else:
                runrulesetname = ruleset["Ruleset name"]

            if connectorname:
                runconnectorname = connectorname
            else:
                runconnectorname = ruleset["Connector name"]
        else:
            runrulesetname = ruleset["Ruleset name"]
            runconnectorname = ruleset["Connector name"]

        if envname:
            runenvname = envname
        else:
            runenvname = ruleset["Environent name"]

        ruleret = ruleset_add(
                    p_engine,
                    runrulesetname, runconnectorname,
                    runenvname)
        ret = ret + ruleret

        if ruleret == 0:
            for meta in ruleset["Metadata"]:

                if meta["table"]:
                    if meta["custom_sql"] == "None":
                        meta["custom_sql"] = None

                    if meta["where_clause"] == "None":
                        meta["where_clause"] = None

                    params = {
                        "rulesetname": runrulesetname,
                        "metaname": meta["meta_name"],
                        "custom_sql": meta["custom_sql"],
                        "where_clause": meta["where_clause"],
                        "key_column": meta["key_column"],
                        "envname": runenvname,
                        "having_clause": None
                    }
                else:
                    params = {
                        "rulesetname": runrulesetname,
                        "metaname": meta["meta_name"],
                        "file_format": meta["file_format"],
                        "file_delimiter": meta["file_delimiter"],
                        "file_eor": meta["file_eor"],
                        "envname": runenvname,
                        "file_enclosure": meta["file_enclosure"],
                        "file_name_regex": meta["file_name_regex"]
                    }

                ret = ret + ruleset_addmeta(p_engine, params, None)

            for column in ruleset["Columns"]:
                if column["is_masked"] == "Y":
                    colret = column_setmasking(
                                p_engine,
                                runrulesetname,
                                runenvname,
                                column["Metadata name"],
                                column["Column name"],
                                column["Alg name"],
                                column["Domain name"],
                                column["dateformat"],
                                column["idmethod"])
                    ret = ret + colret
                else:
                    colret = column_unsetmasking(
                                p_engine,
                                runrulesetname,
                                runenvname,
                                column["Metadata name"],
                                column["Column name"])
                    ret = ret + colret

    return ret


def ruleset_check(p_engine, inputfile):
    rulesets = json.load(inputfile)
    ret = 0
    for ruleset in rulesets:
        ret = ret + ruleset_worker(
                        p_engine=p_engine,
                        rulesetname=ruleset["Ruleset name"],
                        envname=ruleset["Environent name"],
                        ruleset=ruleset,
                        function_to_call="do_check")
    return ret


def do_check(**kwargs):
    """
    Compare
    """

    ruleref = kwargs.get('ruleref')
    rulelist = kwargs.get('rulelist')
    envlist = DxEnvironmentList
    envname = kwargs.get('envname')
    ruleset = kwargs.get('ruleset')
    rulesetname = kwargs.get('rulesetname')
    p_engine = kwargs.get('p_engine')

    connname = ruleset["Connector name"]

    ruleobj = rulelist.get_by_ref(ruleref)
    connobj = DxConnectorsList.get_by_ref(ruleobj.connectorId)

    if connobj:
        envobj = envlist.get_by_ref(connobj.environment_id)
        connector_name = connobj.connector_name
        environment_name = envobj.environment_name
    else:
        connector_name = 'N/A'
        environment_name = 'N/A'

    retcol = 0

    metalist = DxMetaList()
    metalist.LoadMeta(ruleobj.ruleset_id)

    rettab = 0

    for meta in ruleset["Metadata"]:
        metalist_ref = metalist.get_MetadataId_by_name(meta["meta_name"], 1)
        if metalist_ref:
            rettab = rettab + 1
        else:
            print_error("Missing meta %s" % meta["meta_name"])

    for col in ruleset["Columns"]:
        count = [ x for x in ruleset["Columns"] if col["Metadata name"] == x["Metadata name"] ]
        rc = column_check(p_engine, rulesetname, envname, col, len(count))
        if rc != 0:
            retcol = retcol + 1


    if (ruleobj.ruleset_name == rulesetname) and \
       (connector_name == connname) and \
       (environment_name == envname) and \
       (retcol == 0) and \
       (rettab == len(ruleset["Metadata"])):
        print_message("Ruleset definition in engine is matching import file")
        return 0
    else:
        print_error("There are difference between engine and import file")
        return 1
