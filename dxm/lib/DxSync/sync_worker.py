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
# Copyright (c) 2018,2019 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : December 2018


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
import pickle
import os
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxSync.DxSyncList import DxSyncList
from dxm.lib.DxSync.DxSync import DxSync


supported_sync_objects_type = [
 'algorithm',
 'global_object',
 'key',
 'domain',
 'masking_job',
 'database_ruleset', 
 'file_ruleset',
 'database_connector',
 'file_connector'
]


def sync_export(p_engine, p_username,  objecttype, objectname, envname, path):
    """
    Print list of syncable objects
    param1: p_engine: engine name from configuration
    param2: objecttype: objecttype to list, all if None
    param3: objectname: objectname to list_table_details
    param4: format: output format
    return 0 if objecttype found
    """

    return sync_worker(p_engine, p_username,  objecttype, objectname, envname, "do_export",
                       path=path)


def do_export(**kwargs):
    """
    Run object export function for passed object
    object: syncable object DxSync
    name: object name
    path: path to export location
    return 0 if object exported
    return 1 if there where issues
    """
    syncobj = kwargs.get('object')
    name = kwargs.get('name')
    path = kwargs.get('path')
    # print(name)
    # print(path)
    # print(kwargs)
    return syncobj.export(name, path)


def sync_list(p_engine, p_username,  objecttype, objectname, envname, format):
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
                    ("Env name",    32),
                    ("Object name", 32),
                    ("Revision",    50)
                  ]
    data.create_header(data_header)
    data.format_type = format

    ret = sync_worker(p_engine, p_username,  objecttype, objectname, envname, "do_list",
                      data=data)

    print("")
    print (data.data_output(False))
    print("")

    return ret


def do_list(**kwargs):
    """
    Add object information to data object
    engine_obj: Masking engine object
    object: syncable object DxSync
    name: object name
    envname: environment name
    data: output data object
    return 0
    """
    engine_obj = kwargs.get('engine_obj')
    syncobj = kwargs.get('object')
    name = kwargs.get('name')
    envname = kwargs.get('envname')
    data = kwargs.get('data')

    data.data_insert(
                      engine_obj.get_name(),
                      syncobj.object_type,
                      envname,
                      name,
                      syncobj.revision_hash
                    )
    return 0

def sync_worker(p_engine, p_username,  objecttype, objectname, envname,
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

    enginelist = get_list_of_engines(p_engine, p_username)

    # objectname = "RandomValueLookup"
    # objectname = None
    ret = 0

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        synclist = DxSyncList(objecttype)

        if (objecttype is None or objecttype.lower() == "algorithm") \
           and envname is None:
            if objectname:
                alglist = [objectname]
            else:
                alglist = synclist.get_all_algorithms()

            for syncref in alglist:
                syncobj = synclist.get_object_by_type_name(
                                        "algorithm", syncref)
                if syncobj:

                    dynfunc = globals()[function_to_call]
                    ret = ret + dynfunc(
                        object=syncobj,
                        engine_obj=engine_obj,
                        envname='global',
                        name=syncref, **kwargs)

        if objecttype is None or objecttype.lower() == "database_connector" \
           or objecttype.lower() == "file_connector":

            envlist = DxEnvironmentList()
            connlist = DxConnectorsList(envname)

            if objecttype is None:
                objtypelist = ["database_connector", "file_connector"]
            else:
                objtypelist = [objecttype]

            for objtype in objtypelist:

                if objectname:
                    connbynameref = connlist.get_connectorId_by_name(
                                        objectname, False)
                    if connbynameref:
                        syncconnref = int(connbynameref[1:])
                        if synclist.get_object_by_type_name(
                                                objtype,
                                                syncconnref):
                            connrefs = [syncconnref]
                        else:
                            connrefs = []
                    else:
                        connrefs = []
                else:
                    connrefs = synclist.get_all_object_by_type(objtype)


                for syncref in connrefs:
                    syncobj = synclist.get_object_by_type_name(
                                        objtype, syncref)
                    if syncobj.object_type == 'DATABASE_CONNECTOR':
                        connobj = connlist.get_by_ref("d" + str(syncref))
                    else:
                        connobj = connlist.get_by_ref("f" + str(syncref))

                    if connobj is None:
                        # limited by env
                        continue
                    envobj = envlist.get_by_ref(connobj.environment_id)

                    dynfunc = globals()[function_to_call]
                    ret = ret + dynfunc(
                        object=syncobj,
                        engine_obj=engine_obj,
                        envname=envobj.environment_name,
                        name=connobj.connector_name,
                        **kwargs)

        if objecttype is None or objecttype.lower() == "database_ruleset" \
           or objecttype == "file_ruleset":

            envlist = DxEnvironmentList()
            connlist = DxConnectorsList(envname)
            rulesetList = DxRulesetList(envname)

            if objecttype is None:
                objtypelist = ["database_ruleset", "file_ruleset"]
            else:
                objtypelist = [objecttype]

            for objtype in objtypelist:

                if objectname:
                    rulesetrefs = []
                    rulesetref = rulesetList.get_all_rulesetId_by_name(
                                                objectname, verbose=False)
                    if rulesetref:
                        for rsref in rulesetref:
                            if synclist.get_object_by_type_name(
                                                objtype, rsref):
                                rulesetrefs.append(rsref)
                            else:
                                rulesetrefs = []
                    else:
                        rulesetrefs = []
                else:
                    rulesetrefs = synclist.get_all_object_by_type(objtype)

                for syncref in rulesetrefs:
                    syncobj = synclist.get_object_by_type_name(objtype,
                                                               syncref)
                    rulesetobj = rulesetList.get_by_ref(syncref)
                    if rulesetobj is None:
                        # limited by env
                        continue
                    connobj = connlist.get_by_ref(rulesetobj.connectorId)
                    envobj = envlist.get_by_ref(connobj.environment_id)
                    dynfunc = globals()[function_to_call]
                    ret = ret + dynfunc(
                        object=syncobj,
                        engine_obj=engine_obj,
                        envname=envobj.environment_name,
                        name=rulesetobj.ruleset_name,
                        **kwargs)

        if (objecttype is None or objecttype.lower() == "global_object"
           or objecttype == "key" or objecttype == "domain") \
           and envname is None:

            if objecttype is None:
                objtypelist = ["global_object", "key", "domain"]
            else:
                objtypelist = [objecttype]

            for objtype in objtypelist:
                if objectname:
                    objlist = [objectname]
                else:
                    objlist = synclist.get_all_object_by_type(objtype)
                for syncref in objlist:
                    syncobj = synclist.get_object_by_type_name(objtype,
                                                               syncref)
                    if syncobj:

                        dynfunc = globals()[function_to_call]
                        ret = ret + dynfunc(
                            object=syncobj,
                            engine_obj=engine_obj,
                            envname='global',
                            name=syncref, **kwargs)

        if objecttype is None or objecttype.lower() == "masking_job":

            envlist = DxEnvironmentList()
            joblist = DxJobsList()
            joblist.LoadJobs(envname)
            connlist = DxConnectorsList(envname)
            rulesetlist = DxRulesetList(envname)

            if objectname:
                jobref = joblist.get_jobId_by_name(objectname, verbose=False)
                if synclist.get_object_by_type_name("masking_job", jobref):
                    jobrefs = [jobref]
                else:
                    jobrefs = []
            else:
                jobrefs = synclist.get_all_object_by_type("masking_job")

            for syncref in jobrefs:
                syncobj = synclist.get_object_by_type_name("masking_job",
                                                           syncref)
                jobobj = joblist.get_by_ref(syncref)
                if envname and jobobj is None:
                    # limited by env
                    continue
                rulesetobj = rulesetlist.get_by_ref(jobobj.ruleset_id)
                connectorobj = connlist.get_by_ref(rulesetobj.connectorId)
                envobj = envlist.get_by_ref(connectorobj.environment_id)
                dynfunc = globals()[function_to_call]
                ret = ret + dynfunc(
                    object=syncobj,
                    engine_obj=engine_obj,
                    envname=envobj.environment_name,
                    name=jobobj.job_name,
                    **kwargs)

    return ret


def sync_import(p_engine, p_username,  envname, inputfile, inputpath, force):
    """
    Load algorithm from file
    param1: p_engine: engine name from configuration
    param2: inputfile: input file
    param3: force: overwrite object
    return 0 if OK
    """

    ret = 0
    enginelist = get_list_of_engines(p_engine, p_username)

    if inputfile is None and inputpath is None:
        print_error("Inputfile or inputpath parameter is required")
        return 1

    list_of_opened_files = []

    if inputpath:
        for f in os.listdir(inputpath):
            fullpath = os.path.join(inputpath, f)
            if os.path.isfile(fullpath):
                fh = open(fullpath, "rb")
                list_of_opened_files.append(fh)
    else:
        if inputfile:
            list_of_opened_files = [inputfile]

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        if envname:
            environment_id = envlist.get_environmentId_by_name(envname)
        else:
            environment_id = None


        for i in list_of_opened_files:
            syncobj = DxSync(engine_obj)
            ret = ret + syncobj.importsync(i, environment_id, force)

    return ret
