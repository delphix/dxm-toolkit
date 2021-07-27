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

from dxm.lib.DxUser.DxUser import DxUser
from dxm.lib.DxUser.DxUser import DxUserNonAdmin
from dxm.lib.DxUser.DxUserList import DxUserList
from dxm.lib.DxRole.DxRoleList import DxRoleList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxAppSetting.DxAppSettingList import DxAppSettingList


def user_delete(p_engine, username, force):
    """
    Delete user from Engine
    param1: p_engine: engine name from configuration
    param2: username: user name to delete
    param3: force: force deletion of user with admin privilege
    return 0 if user deleted
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
        userlist = DxUserList()

        userref = userlist.get_userId_by_name(username)

        if userref is not None:
            if userlist.delete(userref, force) != 0:
                print_error("Problem with deleting user %s" % username)
                logger.debug("Problem with deleting user %s" % username)
                ret = ret + 1
                continue
        else:
            print_error("User %s not found" % username)
            logger.debug("User %s not found" % username)

def user_update(p_engine, username, firstname, lastname, email, password,
             user_type, user_environments, user_role):
    """
    Update user in Engine
    param1: p_engine: engine name from configuration
    param2: username: user name to add
    param3: firstname: user first name to add
    param4: lastname: user last name to add
    param5: email: user email to add
    param6: password: user password to add
    param7: user_type: user type (admin / nonadmin)
    param8: user_environments: list of comma separated environments
    param9: user_role: user role name
    return 0 if user updated
    """

    ret = 0
    update = 0
    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine)
    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue


        userlist = DxUserList()
        userref = userlist.get_userId_by_name(username)

        if userref is None:
            print_error("User %s not found" % username)
            logger.debug("User %s not found" % username)
            ret = ret + 1
            continue

        userobj = userlist.get_by_ref(userref)

        if user_type is not None:
            update = 1
            if user_type == 'nonadmin':
                if user_role is None:
                    print_error("User role is required for non-admin user")
                    return 1
                rolelist = DxRoleList()
                roleref = rolelist.get_roleId_by_name(user_role)
                if roleref is None:
                    print_error("Role name %s not found" % user_role)
                    logger.debug("Role name %s not found" % user_role)
                    ret = ret + 1
                    continue

                envreflist = []
                if user_environments is not None:
                    envlist = DxEnvironmentList()
                    envnamelist = user_environments.split(',')
                    for envname in envnamelist:
                        envref = envlist.get_environmentId_by_name(envname)
                        if envref is None:
                            ret = ret + 1
                            return 1
                        else:
                            envreflist.append(envref)


                userobj.is_admin = False
                nap = DxUserNonAdmin(role_id=roleref, environment_ids=envreflist)
                userobj.non_admin_properties = nap
            else:
                userobj.is_admin = True
                userobj.delete_nap()
                print_message(userobj)

        if firstname is not None:
            update = 1
            userobj.first_name = firstname

        if lastname is not None:
            update = 1
            userobj.last_name = lastname

        if email is not None:
            update = 1
            userobj.email = email

        if password is not None:
            update = 1
            try:
                userobj.password = password
            except ValueError as e:
                print_error(str(e))
                ret = ret + 1
                return ret

        if update == 1:
            ret = ret + userobj.update()
        else:
            print_error("No values set for update.")
            ret = ret + 1

    return ret


def user_add(p_engine, username, firstname, lastname, email, password,
             user_type, user_environments, user_role):
    """
    Add user to Engine
    param1: p_engine: engine name from configuration
    param2: username: user name to add
    param3: firstname: user first name to add
    param4: lastname: user last name to add
    param5: email: user email to add
    param6: password: user password to add
    param7: user_type: user type (admin / nonadmin)
    param8: user_environments: list of comma separated environments
    param9: user_role: user role name
    return 0 if user added
    """

    ret = 0
    logger = logging.getLogger()
    if user_type == 'nonadmin':
        if user_role is None:
            print_error("User role is required for non-admin user")
            return 1

    enginelist = get_list_of_engines(p_engine)
    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        if (engine_obj.version_ge('6.0.0')):
            from masking_api_60.models.non_admin_properties import NonAdminProperties
        else:
            from masking_api_53.models.non_admin_properties import NonAdminProperties


        userobj = DxUser(engine_obj)

        if user_type == 'nonadmin':
            rolelist = DxRoleList()
            roleref = rolelist.get_roleId_by_name(user_role)
            if roleref is None:
                print_error("Role name %s not found" % user_role)
                logger.debug("Role name %s not found" % user_role)
                ret = ret + 1
                continue


            envreflist = []

            if user_environments is not None:
                envlist = DxEnvironmentList()
                envnamelist = user_environments.split(',')
                for envname in envnamelist:
                    envref = envlist.get_environmentId_by_name(envname)
                    if envref is None:
                        ret = ret + 1
                        return 1
                    else:
                        envreflist.append(envref)

            is_admin = False
            nap = DxUserNonAdmin(roleref, envreflist)
        else:
            is_admin = True
            nap = None

        try:
            userobj.create_user(user_name = username, password = password, first_name=firstname, last_name=lastname,
                                email=email, is_admin=is_admin, non_admin_properties=nap)
        except ValueError as e:
            print_error(str(e))
            ret = ret + 1
            return ret

        

        userlist = DxUserList()
        ret = ret + userlist.add(userobj)

    return ret

def user_list(p_engine, format, username):
    """
    Print list of users
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: username: user name to list, all if None
    return 0 if role found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("User name", 30),
                    ("First name", 30),
                    ("Last name", 30),
                    ("E-mail", 30),
                    ("Auth type", 10),
                    ("Principal", 30),
                    ("Role name", 30),
                    ("Locked", 6),
                    ("Environment list", 30)
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue
        userlist = DxUserList()
        rolelist = DxRoleList()
        envlist = DxEnvironmentList()

        # check if ldap is configured
        appsettingslist = DxAppSettingList()
        ldapobj = appsettingslist.get_appSetting_by_group_and_name(
                    'ldap', 'Enable')

        if ldapobj.setting_value == 'true':
            msadobj = appsettingslist.get_appSetting_by_group_and_name(
                    'ldap', 'MsadDomain')
        else:
            msadobj = None

        if username is None:
            users = userlist.get_allref()
        else:
            user = userlist.get_userId_by_name(username)

            if user is None:
                ret = ret + 1
                continue
            users = [user]

        for userref in users:
            userobj = userlist.get_by_ref(userref)

            if not userobj.is_admin:
                roleobj = rolelist.get_by_ref(
                    userobj.non_admin_properties.role_id)
                if roleobj is not None:
                    rolename = roleobj.role_name
                else:
                    rolename = 'Not Found'
            else:
                rolename = 'Administrator'

            if userobj.non_admin_properties is not None:
                if userobj.non_admin_properties.environment_ids:
                    envs = ';'.join(
                        [envlist.get_by_ref(x).environment_name
                         for x in userobj.non_admin_properties.environment_ids]
                        )
                else:
                    envs = ''
            else:
                envs = ''

            if userobj.is_locked is not None:
                if userobj.is_locked is True:
                    locked = 'Locked'
                else:
                    locked = 'Open'
            else:
                locked = 'N/A'

            if msadobj is None:
                authtype = 'NATIVE'
                principal = ''
            else:
                authtype = 'LDAP'
                principal = '{}@{}'.format(
                    userobj.user_name, msadobj.setting_value)

            data.data_insert(
                              engine_tuple[0],
                              userobj.user_name,
                              userobj.first_name,
                              userobj.last_name,
                              userobj.email,
                              authtype,
                              principal,
                              rolename,
                              locked,
                              envs
                            )
    print("")
    print (data.data_output(False))
    print("")
    return ret
