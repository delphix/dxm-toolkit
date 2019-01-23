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
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxSync.DxSyncList import DxSyncList
from dxm.lib.DxSync.DxSync import DxSync

import sys

def sync_export(p_engine, objecttype, objectname, envname, path=None):
    """
    Print list of syncable objects
    param1: p_engine: engine name from configuration
    param2: objecttype: objecttype to list, all if None
    param3: objectname: objectname to list_table_details
    param4: format: output format
    return 0 if objecttype found
    """

    return sync_worker(p_engine, objecttype, objectname, envname, "do_export",
                       path=path)


def do_export(**kwargs):
    syncobj = kwargs.get('object')
    name = kwargs.get('name')
    path = kwargs.get('path')

    syncobj.export(name, path)

    return 0


def sync_list(p_engine, objecttype, objectname, envname, format):
    """
    Print list of syncable objects
    param1: p_engine: engine name from configuration
    param2: objecttype: objecttype to list, all if None
    param3: objectname: objectname to list_table_details
    param4: format: output format
    return 0 if objecttype found
    """
    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Object type", 30),
                    ("Object name", 32),
                    ("Revision",    50)
                  ]
    data.create_header(data_header)
    data.format_type = format

    ret = sync_worker(p_engine, objecttype, objectname, envname, "do_list",
                      data=data)

    print("")
    print (data.data_output(False))
    print("")

    return ret


def do_list(**kwargs):
    engine_obj = kwargs.get('engine_obj')
    syncobj = kwargs.get('object')
    name = kwargs.get('name')
    data = kwargs.get('data')

    data.data_insert(
                      engine_obj.get_name(),
                      syncobj.object_type,
                      name,
                      syncobj.revision_hash
                    )
    return 0

def sync_worker(p_engine, objecttype, objectname, envname,
                function_to_call, **kwargs):
    """
    Run an action for list of syncable objects
    param1: p_engine: engine name from configuration
    param2: objecttype: objecttype to list, all if None
    param3: objectname: objectname to list_table_details
    param4: function_to_call
    return 0 if objecttype found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    # objectname = "RandomValueLookup"
    # objectname = None
    ret = 0

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue


        synclist = DxSyncList(objecttype)

        if objecttype is None or objecttype == "algorithm":

            if objectname:
                alglist = [objectname]
            else:
                alglist = synclist.get_all_algorithms()

            for syncref in alglist:
                syncobj = synclist.get_object_by_type_name("algorithm", syncref)
                if syncobj:

                    dynfunc = globals()[function_to_call]
                    ret = ret + dynfunc(
                        object=syncobj,
                        engine_obj=engine_obj,
                        name=syncref, **kwargs)


        if objecttype is None or objecttype == "database_connector":

            envlist = DxEnvironmentList()
            connlist = DxConnectorsList(envname)

            if objectname:
                connbynameref = connlist.get_connectorId_by_name(
                                    objectname, False)
                if connbynameref and \
                   connlist.get_by_ref(connbynameref).is_database:
                    syncconnref = int(connbynameref[1:])
                    if synclist.get_object_by_type_name(
                                            "database_connector",
                                            syncconnref):
                        dbconnrefs = [syncconnref]
                    else:
                        dbconnrefs = []
                else:
                    dbconnrefs = []
            else:
                dbconnrefs = synclist.get_all_object_by_type(
                                            "database_connector")


            for syncref in dbconnrefs:
                syncobj = synclist.get_object_by_type_name(
                                        "database_connector", syncref)
                connobj = connlist.get_by_ref("d" + str(syncref))
                envobj = envlist.get_by_ref(connobj.environment_id)

                dynfunc = globals()[function_to_call]
                ret = ret + dynfunc(
                    object=syncobj,
                    engine_obj=engine_obj,
                    name=envobj.environment_name + "_"
                    + connobj.connector_name,
                    **kwargs)


        if objecttype is None or objecttype == "file_connector":

            envlist = DxEnvironmentList()
            connlist = DxConnectorsList(envname)


            if objectname:
                connbynameref = connlist.get_connectorId_by_name(
                                    objectname, False)
                if connbynameref and \
                   not connlist.get_by_ref(connbynameref).is_database:
                    syncconnref = int(connbynameref[1:])
                    if synclist.get_object_by_type_name(
                                            "file_connector", syncconnref):
                        fileconnrefs = [syncconnref]
                    else:
                        fileconnrefs = []
                else:
                    fileconnrefs = []
            else:
                fileconnrefs = synclist.get_all_object_by_type(
                                            "file_connector")


            for syncref in fileconnrefs:
                syncobj = synclist.get_object_by_type_name(
                                        "file_connector", syncref)
                connobj = connlist.get_by_ref("f" + str(syncref))
                envobj = envlist.get_by_ref(connobj.environment_id)
                dynfunc = globals()[function_to_call]
                ret = ret + dynfunc(
                    object=syncobj,
                    engine_obj=engine_obj,
                    name=envobj.environment_name + "_"
                    + connobj.connector_name,
                    **kwargs)


        if objecttype is None or objecttype == "database_ruleset":

            envlist = DxEnvironmentList()
            connlist = DxConnectorsList(envname)
            rulesetList = DxRulesetList(envname)

            if objectname:
                rulesetref = rulesetList.get_rulesetId_by_name(objectname)
                if synclist.get_object_by_type_name(
                                        "database_ruleset", rulesetref):

                    rulesetrefs = [rulesetref]
                else:
                    rulesetrefs = []
            else:
                rulesetrefs = synclist.get_all_object_by_type(
                                            "database_ruleset")

            for syncref in rulesetrefs:
                syncobj = synclist.get_object_by_type_name(
                                        "database_ruleset", syncref)
                rulesetobj = rulesetList.get_by_ref(syncref)
                connobj = connlist.get_by_ref(rulesetobj.connectorId)
                envobj = envlist.get_by_ref(connobj.environment_id)
                dynfunc = globals()[function_to_call]
                ret = ret + dynfunc(
                    object=syncobj,
                    engine_obj=engine_obj,
                    name=envobj.environment_name + "_"
                    + rulesetobj.ruleset_name,
                    **kwargs)

        if objecttype is None or objecttype == "file_ruleset":

            envlist = DxEnvironmentList()
            connlist = DxConnectorsList(envname)
            rulesetList = DxRulesetList(envname)

            if objectname:
                rulesetref = rulesetList.get_rulesetId_by_name(objectname)
                if synclist.get_object_by_type_name(
                                        "file_ruleset", rulesetref):

                    rulesetrefs = [rulesetref]
                else:
                    rulesetrefs = []
            else:
                rulesetrefs = synclist.get_all_object_by_type(
                                            "file_ruleset")

            for syncref in rulesetrefs:
                syncobj = synclist.get_object_by_type_name(
                                        "file_ruleset", syncref)
                rulesetobj = rulesetList.get_by_ref(syncref)
                connobj = connlist.get_by_ref(rulesetobj.connectorId)
                envobj = envlist.get_by_ref(connobj.environment_id)
                dynfunc = globals()[function_to_call]
                ret = ret + dynfunc(
                    object=syncobj,
                    engine_obj=engine_obj,
                    name=envobj.environment_name + "_"
                    + rulesetobj.ruleset_name,
                    **kwargs)

    return ret


def algorithm_worker(p_engine, algname, **kwargs):
    """
    Select an algorithm and run action on it
    param1: p_engine: engine name from configuration
    param2: algname: algorithm name
    kwargs: parameters to pass including function name to call
    return 0 if algname found
    """

    ret = 0

    function_to_call = kwargs.get('function_to_call')

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        domainlist = DxDomainList()
        domainlist.LoadDomains()

        alglist = DxAlgorithmList()

        algref_list = []


        algobj = alglist.get_by_ref(algname)
        if algobj is None:
            ret = ret + 1
            continue

        dynfunc = globals()[function_to_call]
        if dynfunc(algobj=algobj, engine_obj=engine_obj, **kwargs):
            ret = ret + 1

    return ret


def sync_import(p_engine, target_envname, inputfile):
    """
    Load algorithm from file
    param1: p_engine: engine name from configuration
    param2: inputfile: input file
    return 0 if OK
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

        syncobj = DxSync(engine_obj)
        syncobj.importsync(None)
