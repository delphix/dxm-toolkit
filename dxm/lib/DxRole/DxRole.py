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


class DxRole(object):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #Role.__init__(self)
        self.__logger = logging.getLogger()
        self.__engine = engine
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.role import Role
            from masking_api_60.api.role_api import RoleApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.role import Role
            from masking_api_53.api.role_api import RoleApi
            from masking_api_53.rest import ApiException

        self.__api = RoleApi
        self.__model = Role
        self.__apiexc = ApiException
        self.__obj = None

    def from_role(self, role):
        self.__obj = role

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None


    @property
    def role_name(self):
        if self.obj is not None:
            return self.obj.role_name
        else:
            return None

    @role_name.setter
    def role_name(self, role_name):
        if self.__obj is not None:
            self.__obj.role_name = role_name
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
