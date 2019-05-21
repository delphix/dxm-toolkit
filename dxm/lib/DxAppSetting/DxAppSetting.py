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
from masking_apis.models.application_settings import ApplicationSettings
from masking_apis.apis.application_settings_api import ApplicationSettingsApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxAppSetting(ApplicationSettings):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        ApplicationSettings.__init__(self)
        self.__logger = logging.getLogger()
        self.__engine = engine

    def from_role(self, appsetting):
        """
        Copy properties from ApplicationSettings object into DxRole
        :param appsetting: ApplicationSettings object
        """
        self.__dict__.update(appsetting.__dict__)

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
