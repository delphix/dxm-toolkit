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
# Date    : March 2018


import logging
#from masking_api_60.models.application import Application
#from masking_api_60.api.application_api import ApplicationApi
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.masking_api.api.application_api import ApplicationApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxApplication.Application_mixin import Application_mixin


class DxApplication(Application_mixin):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #Application.__init__(self, application_name='init')
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxApplication object")

        self.__api = ApplicationApi
        self.__apiexc = ApiException
        self._obj = None


    def create_application(self, application_name):
        """
        Copy properties from application object into DxApplication
        :param app: Application object
        """  
        self._obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.application_name = application_name


    def load_obj(self, obj):
        """
        Assign a SDK object to _obj
        :param app: Application object
        """
        self._obj = obj
        self._obj.swagger_types = self.swagger_types
        self._obj.swagger_map = self.swagger_map

    def add(self):
        """
        Add application to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.application_name is None):
            print_error("Application name is required")
            self.__logger.error("Application name is required")
            return 1

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("create application input %s" % str(self))
            response = api_instance.create_application(
                self._obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create application response %s"
                                % str(response))

            print_message("Application %s added" % self.application_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    def delete(self):
        """
        Delete application
        return a 0 if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete application name %s"
                                % self.obj.application_name)
            response = api_instance.delete_application(
                self.obj.application_id,
                _request_timeout=self.__engine.get_timeout()
            )
            self.__logger.debug("delete application name response %s"
                                % str(response))
            print_message("Application %s deleted" % self.obj.application_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1