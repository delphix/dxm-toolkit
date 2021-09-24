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
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.environment_api import EnvironmentApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel

class DxEnvironment(object):

    swagger_types = {
        'environment_id': 'int',
        'environment_name': 'str',
        'application_id': 'int',
        'application': 'str',
        'purpose': 'str',
        'is_workflow_enabled': 'bool'
    }

    swagger_map = {
        'environment_id': 'environmentId',
        'environment_name': 'environmentName',
        'application_id': 'applicationId',
        'purpose': 'purpose',
        'is_workflow_enabled': 'isWorkflowEnabled',
        'application': 'application'
    }


    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        
        self.__logger = logging.getLogger()
        self.__engine = engine

        self.__api = EnvironmentApi
        self.__apiexc = ApiException
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
        if self.__engine.version_ge("6.0.0.0"):
            return self.__application_name
        else:
            return self.__obj.application

    @application_name.setter
    def application_name(self, application_name):
        self.__application_name = application_name
        if self.__engine.version_le("5.3.9.9"):
            self.__obj.application = application_name

    @property
    def application_id(self):
        if self.__obj is not None:
            return self.__obj.application_id
        else:
            return None

    @application_id.setter
    def application_id(self, application_id):
        if self.__obj is not None:
            self.__obj.application_id = application_id
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def purpose(self):
        if self.__obj is not None:
            return self.__obj.purpose
        else:
            return None

    @purpose.setter
    def purpose(self, purpose):
        if self.__obj is not None:
            self.__obj.purpose = purpose
        else:
            raise ValueError("Object needs to be initialized first")


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
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map

    def create_environment(self, environment_name, application_name, purpose):
        """
        Create an environment object
        :param app: Application object
        """  

        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)

        if self.__engine.version_ge("6.0.0.0"):
            appList = DxApplicationList()
            appList.LoadApplications()
            application_id = appList.get_applicationId_by_name(application_name)
            self.environment_name=environment_name
            self.purpose=purpose
            self.application_id = application_id[0]
        else:
            self.environment_name=environment_name
            self.purpose=purpose
            self.application_name = application_name

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
        except self.__apiexc as e:
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
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
