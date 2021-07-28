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
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.application_settings_api import ApplicationSettingsApi
from dxm.lib.masking_api.rest import ApiException

class DxAppSetting(object):

    swagger_types = {
        'setting_id': 'int',
        'setting_group': 'str',
        'setting_name': 'str',
        'setting_value': 'str'
    }

    swagger_map = {
        'setting_id': 'settingId',
        'setting_group': 'settingGroup',
        'setting_name': 'settingName',
        'setting_value': 'settingValue'
    }

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #ApplicationSettings.__init__(self)
        self.__logger = logging.getLogger()
        self.__engine = engine

        self.__api = ApplicationSettingsApi
        self.__apiexc = ApiException
        self.__obj = None

    def from_role(self, appsetting):
        self.__obj = appsetting
        self.__obj.swagger_map = self.swagger_map
        self.__obj.swagger_types = self.swagger_types

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None


    @property
    def setting_name(self):
        if self.obj is not None:
            return self.obj.setting_name
        else:
            return None

    @setting_name.setter
    def setting_name(self, setting_name):
        if self.__obj is not None:
            self.__obj.setting_name = setting_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def setting_value(self):
        if self.obj is not None:
            return self.obj.setting_value
        else:
            return None

    @setting_value.setter
    def setting_value(self, setting_value):
        if self.__obj is not None:
            self.__obj.setting_value = setting_value
        else:
            raise ValueError("Object needs to be initialized first")

    # def add(self):
    #     """
    #     Add environment to Masking engine and print status message
    #     return a None if non error
    #     return 1 in case of error
    #     """
    #
    #     if (self.environment_name is None):
    #         print "Environment name is required"
    #         self.__logger.error("Environment name is required")
    #         return 1
    #
    #     if (self.application is None):
    #         print "Application name is required"
    #         self.__logger.error("Application name is required")
    #         return 1
    #
    #     if (self.purpose is None):
    #         print "Purpose is required"
    #         self.__logger.error("Purpose is required")
    #         return 1
    #
    #     api_instance = EnvironmentApi(self.__engine.api_client)
    #
    #     try:
    #         self.__logger.debug("create environment input %s" % str(self))
    #         response = api_instance.create_environment(
    #             self,
    #             _request_timeout=self.__engine.get_timeout())
    #         self.__logger.debug("create environment response %s"
    #                             % str(response))
    #
    #         self.environment_id = response.environment_id
    #         self.purpose = response.purpose
    #         self.is_workflow_enabled = response.is_workflow_enabled
    #         print_message("Environment %s added" % self.environment_name)
    #     except ApiException as e:
    #         print_error(e.body)
    #         self.__logger.error(e)
    #         return 1
    #
    # def delete(self):
    #     """
    #     Delete environment to Masking engine and print status message
    #     return a None if non error
    #     return 1 in case of error
    #     """
    #
    #     api_instance = EnvironmentApi(self.__engine.api_client)
    #
    #     try:
    #         self.__logger.debug("delete environment id %s"
    #                             % self.environment_id)
    #         response = api_instance.delete_environment(
    #             self.environment_id,
    #             _request_timeout=self.__engine.get_timeout())
    #         self.__logger.debug("delete environment response %s"
    #                             % str(response))
    #         print_message("Environment %s deleted" % self.environment_name)
    #     except ApiException as e:
    #         print_error(e.body)
    #         self.__logger.error(e)
    #         return 1
