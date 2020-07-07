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
# Date    : March 2018


import logging
from dxm.lib.DxApplication.DxApplicationList import DxApplicationList
from masking_api_60.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxEnvironment(object):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        
        self.__logger = logging.getLogger()
        self.__engine = engine
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.environment import Environment
            from masking_api_60.api.environment_api import EnvironmentApi
        else:
            from masking_api_53.models.environment import Environment
            from masking_api_53.api.environment_api import EnvironmentApi

        self.__api = EnvironmentApi
        self.__model = Environment
        self.__obj = None
        self.__application_name = None

    @property
    def environment_id(self):
        if self.__obj is not None:
            return self.__obj.environment_id
        else:
            return None

    @property
    def application_name(self):
        if hasattr(self.__model, "application_id"):
            return self.__application_name
        else:
            return self.__obj.application

    @application_name.setter
    def application_name(self, application_name):
        self.__application_name = application_name


    @property
    def environment_name(self):
        if self.__obj is not None:
            return self.__obj.environment_name
        else:
            return None

    @environment_name.setter
    def environment_name(self, environment_name):
        if self.__obj is not None:
            self.__obj.environment_name = environment_name
        else:
            raise ValueError("Object needs to be initialized first")


    def from_environment(self, env):
        """
        Copy properties from environemnt object into DxEnvironment
        :param env: Environment object
        """
        self.__obj = env

    def create_environment(self, environment_name, application_name, purpose):
        """
        Create an environment object
        :param app: Application object
        """  

        if hasattr(self.__model, "application_id"):
            appList = DxApplicationList()
            appList.LoadApplications()
            application_id = appList.get_applicationId_by_name(application_name)
            self.__obj = self.__model(environment_name=environment_name, application_id=application_id[0], purpose=purpose)
        else:
            self.__obj = self.__model(environment_name=environment_name, application=application_name, purpose=purpose)

    def add(self):
        """
        Add environment to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        # if (self.environment_name is None):
        #     print_error("Environment name is required")
        #     self.__logger.error("Environment name is required")
        #     return 1

        # if (self.application is None):
        #     print_error("Application name is required")
        #     self.__logger.error("Application name is required")
        #     return 1

        # if (self.purpose is None):
        #     print_error("Purpose is required")
        #     self.__logger.error("Purpose is required")
        #     return 1


        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("create environment input %s" % str(self.__obj))
            response = api_instance.create_environment(
                self.__obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create environment response %s"
                                % str(response))

            self.__obj = response
            print_message("Environment %s added" % self.environment_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete environment to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete environment id %s"
                                % self.environment_id)
            response = api_instance.delete_environment(
                self.environment_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("delete environment response %s"
                                % str(response))
            print_message("Environment %s deleted" % self.environment_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
