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
from masking_api_60.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine





class DxApplication(object):


    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #Application.__init__(self, application_name='init')
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxApplication object")
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.api.application_api import ApplicationApi
            from masking_api_60.models.application import Application
        else:
            from masking_api_53.api.application_api import ApplicationApi
            from masking_api_53.models.application import Application

        self.__api = ApplicationApi
        self.__model = Application
        self.__obj = None

    @property
    def application_name(self):
        if self.__obj is not None:
            return self.__obj.application_name
        else:
            return None

    @application_name.setter
    def application_name(self, application_name):
        if self.__obj is not None:
            self.__obj.application_name = application_name
        else:
            raise ValueError("Object needs to be initialized first")


    def create_application(self, application_name):
        """
        Copy properties from application object into DxApplication
        :param app: Application object
        """  
        self.__obj = self.__model(application_name=application_name)


    def from_obj(self, obj):
        """
        Assign a SDK object to __obj
        :param app: Application object
        """
        self.__obj = obj

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
                self.__obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create application response %s"
                                % str(response))

            print_message("Application %s added" % self.application_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
