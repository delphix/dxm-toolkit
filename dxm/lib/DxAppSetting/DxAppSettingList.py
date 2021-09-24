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
from dxm.lib.DxAppSetting.DxAppSetting import DxAppSetting
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxLogging import print_error
from dxm.lib.masking_api.api.application_settings_api import ApplicationSettingsApi
from dxm.lib.masking_api.rest import ApiException


class DxAppSettingList(object):

    # global list of roles on the class level
    __appSettingGroupList = {}
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
        self.__logger.debug("creating DxAppSettingList object")
        self.LoadAppSettings()

    @classmethod
    def LoadAppSettings(self):
        """
        Load application settings list from Engine into global group list
        return None if OK
        return 1 if error
        """


        self.__api = ApplicationSettingsApi
        self.__apiexc = ApiException

        self.__appSettingGroupList.clear()
        try:
            api_instance = self.__api(self.__engine.api_client)
            applist = paginator(
                        api_instance,
                        "get_all_application_settings",
                        _request_timeout=self.__engine.get_timeout())

            if applist.response_list:
                for c in applist.response_list:
                    setting = DxAppSetting(self.__engine)
                    setting.from_role(c)
                    if c.setting_group not in self.__appSettingGroupList:
                        self.__appSettingGroupList[c.setting_group] = {}
                    self.__appSettingGroupList[c.setting_group][c.setting_name] = setting
            else:
                self.__logger.error("No application settings found")
                print_error("No application settings found")

        except self.__apiexc as e:
            self.__logger.error("Can't load application settings %s" % e.body)
            print_error("Can't load application settings %s" % e.body)
            return 1


    @classmethod
    def get_allgroups(self):
        """
        return a list of all Application groups
        """
        return self.__appSettingGroupList.keys()


    @classmethod
    def get_allSettingForGroup(self, group):
        """
        return a list of all Application settings names in group
        :param group: App settings group name
        return list of application settings
        """

        if group in self.__appSettingGroupList:
            return self.__appSettingGroupList[group].keys()
        else:
            print_error("Group name %s not found" % group)
            self.__logger.error("Group name %s not found" % group)
            return None


    @classmethod
    def get_appSetting_by_group_and_name(self, group, name):
        """
        Return an application setting object for group and name
        :param group: App settings group name
        :param name: App settings name
        return DxAppSetting if found
        return None if not found or not unique
        """

        if group in self.__appSettingGroupList:
            if name in self.__appSettingGroupList[group]:
                return self.__appSettingGroupList[group][name]
            else:
                print_error("Application setting name %s not found" % name)
                self.__logger.error("Application setting name %s not found" % name)
                return None

        else:
            print_error("Group name %s not found" % group)
            self.__logger.error("Group name %s not found" % group)
            return None




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
