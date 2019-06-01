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
# Copyright (c) 2019 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : May 2019


import logging
import sys
from dxm.lib.DxRole.DxRole import DxRole
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from masking_apis.apis.role_api import RoleApi
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error


class DxRoleList(object):

    # global list of roles on the class level
    __roleList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxRoleList object")
        self.LoadRoles()

    @classmethod
    def LoadRoles(self):
        """
        Load roles list from Engine into global list
        return None if OK
        return 1 if error
        """

        self.__roleList.clear()
        try:
            api_instance = RoleApi(self.__engine.api_client)
            rolelist = paginator(
                        api_instance,
                        "get_all_roles",
                        _request_timeout=self.__engine.get_timeout())

            if rolelist.response_list:
                for c in rolelist.response_list:
                    role = DxRole(self.__engine)
                    role.from_role(c)
                    self.__roleList[c.role_id] = role
            else:
                self.__logger.error("No roles found")
                print_error("No roles found")

        except ApiException as e:
            self.__logger.error("Can't load roles %s" % e.body)
            print_error("Can't load roles %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a DxRole object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__roleList[reference]

        except KeyError as e:
            self.__logger.debug("can't find role object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__roleList.keys()

    @classmethod
    def get_roleId_by_name(self, name):
        """
        Return an role id for name
        :param name: Role name
        return role_id if found
        return None if not found or not unique
        """
        roles = get_objref_by_val_and_attribute(name, self,
                                                'role_name')
        if len(roles) < 1:
            print_error("Role %s not found" % name)
            self.__logger.error("Role %s not found " % name)
            return None

        if len(roles) > 1:
            print_error("Role name %s is not unique" % name)
            self.__logger.error("Role %s is not unique" % name)
            return None

        return roles[0]


    # @classmethod
    # def add(self, environment):
    #     """
    #     Add an environment to a list and Engine
    #     :param environment: Environment object to add to Engine and list
    #     return None if OK
    #     """
    #
    #     if (environment.add() is None):
    #         self.__logger.debug("Adding environment %s to list" % environment)
    #         self.__environmentList[environment.environment_id] = environment
    #         return None
    #     else:
    #         return 1
    #
    # @classmethod
    # def delete(self, environmentId):
    #     """
    #     Delete an environment from a list and Engine
    #     :param environmentId: Environment id to delete from Engine and list
    #     return None if OK
    #     """
    #
    #     environment = self.get_by_ref(environmentId)
    #     if environment is not None:
    #         if environment.delete() is None:
    #             return None
    #         else:
    #             return 1
    #     else:
    #         print "Environment with id %s not found" % environmentId
    #         return 1
