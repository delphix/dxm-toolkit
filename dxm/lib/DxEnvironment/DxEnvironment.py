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

import pprint
import logging
from dxm.lib.DxApplication.DxApplicationList import DxApplicationList
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.environment_api import EnvironmentApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxEnvironment.Environment_mixin import Environment_mixin

class DxEnvironment(Environment_mixin):

    

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        
        self.__logger = logging.getLogger()
        self.__engine = engine

        self.__api = EnvironmentApi
        self.__apiexc = ApiException
        self._obj = None
        self.__application_name = None
        self.swagger_types['application'] = 'str'
        self.swagger_map['application'] = 'application'



    @property
    def application_name(self):
        if self.__engine.version_ge("6.0.0.0"):
            return self.__application_name
        else:
            return self._obj.application

    @application_name.setter
    def application_name(self, application_name):
        self.__application_name = application_name
        if self.__engine.version_le("5.3.9.9"):
            self._obj.application = application_name



    def load_object(self, env):
        """
        Copy properties from environemnt object into DxEnvironment
        :param env: Environment object
        """
        self._obj = env
        self._obj.swagger_types = self.swagger_types
        self._obj.swagger_map = self.swagger_map

    def create_environment(self, environment_name, application_name, purpose):
        """
        Create an environment object
        :param app: Application object
        """  

        self._obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)

        if self.__engine.version_ge("6.0.0.0"):
            appList = DxApplicationList()
            appList.LoadApplications()
            application_id = appList.get_applicationId_by_name(application_name)
            self.environment_name=environment_name
            self.purpose=purpose
            self.application_id = application_id[0]
            self.application_name = application_name
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

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("create environment input %s" % str(self._obj))
            response = api_instance.create_environment(
                self._obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create environment response %s"
                                % str(response))

            self._obj = response
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

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()