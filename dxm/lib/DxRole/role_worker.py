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

from dxm.lib.DxRole.DxRole import DxRole
from dxm.lib.DxRole.DxRoleList import DxRoleList




def role_list(p_engine, p_username,  format, rolename):
    """
    Print list of roles
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: rolename: role name to list, all if None
    return 0 if role found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Role name", 30)
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue
        rolelist = DxRoleList()
        # load all objects

        if rolename is None:
            roles = rolelist.get_allref()
        else:
            role = rolelist.get_roleId_by_name(rolename)

            if role is None:
                ret = ret + 1
                continue
            roles = [role]

        for roleref in roles:
            roleobj = rolelist.get_by_ref(roleref)
            data.data_insert(
                              engine_tuple[0],
                              roleobj.role_name
                            )
    print("")
    print (data.data_output(False))
    print("")
    return ret
