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
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines

from dxm.lib.DxApplication.DxApplicationList import DxApplicationList
from dxm.lib.DxApplication.DxApplication import DxApplication


def application_add(p_engine, appname):
    """
    Add application to Masking engine
    param1: p_engine: engine name from configuration
    param2: appname: application name
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1
    # create new object of Application class

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])
        if engine_obj.get_session():
            continue
        applist = DxApplicationList()
        appnew = DxApplication(engine_obj)
        # set a name
        appnew.application_name = appname

        # add Application to engine and list
        # rc is None all is OK

        if applist.add(appnew):
            ret = ret + 1

    return ret


def application_list(p_engine, format, appname):
    """
    Print list of applications
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: appname: application name to list, all if None
    return 0 if application found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Application name", 30),
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])
        if engine_obj.get_session():
            continue
        applist = DxApplicationList()
        # load all objects
        applist.LoadApplications()

        if appname is None:
            applications = applist.get_allref()
        else:
            applications = applist.get_applicationId_by_name(appname)
            if len(applications) == 0:
                ret = ret + 1

        for appref in applications:
            appobj = applist.get_by_ref(appref)
            data.data_insert(
                              engine_tuple[0],
                              appobj.application_name
                            )
        print("")
        print (data.data_output(False))
        print("")
        return ret
