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
# Copyright (c) 2018-2020 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : April 2018


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines

from dxm.lib.DxEnvironment.DxEnvironment import DxEnvironment
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList


def environment_add(p_engine, p_username,  envname, appname, purpose):
    """
    Add application to Masking engine
    param1: p_engine: engine name from configuration
    param2: envname: environment name
    param3: appname: application name
    param4: purpose: environment purpose ( MASK )
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        env = DxEnvironment(engine_obj)
        # set required properties
        env.create_environment(environment_name = envname, application_name = appname, purpose = purpose)


        if envlist.add(env):
            ret = ret + 1

    return ret


def environment_delete(p_engine, p_username,  envname):
    """
    Delete application from Masking engine
    param1: p_engine: engine name from configuration
    param2: envname: environment name
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        envref = envlist.get_environmentId_by_name(envname)
        if envlist.delete(envref):
            ret = ret + 1

    return ret


def environment_list(p_engine, p_username,  format, envname):
    """
    Print list of environments
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: envname: environemnt name to list, all if None
    return 0 if environment found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Environment name", 30),
                    ("Application name", 30)
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue
        envlist = DxEnvironmentList()
        # load all objects
        # envlist.LoadEnvironments()

        if envname is None:
            environments = envlist.get_allref()
        else:
            environment = envlist.get_environmentId_by_name(envname)

            if environment is None:
                ret = ret + 1
                continue
            environments = [environment]

        for envref in environments:
            envobj = envlist.get_by_ref(envref)
            data.data_insert(
                              engine_tuple[0],
                              envobj.environment_name,
                              envobj.application_name
                            )
    print("")
    print (data.data_output(False))
    print("")
    return ret
