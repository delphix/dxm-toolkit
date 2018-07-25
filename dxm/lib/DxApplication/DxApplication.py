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
from masking_apis.models.application import Application
from masking_apis.apis.application_api import ApplicationApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxApplication(Application):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        Application.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxApplication object")

    def from_application(self, app):
        """
        Copy properties from application object into DxApplication
        :param app: Application object
        """
        self.__dict__.update(app.__dict__)

    def add(self):
        """
        Add application to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.application_name is None):
            print "Application name is required"
            self.__logger.error("Application name is required")
            return 1

        api_instance = ApplicationApi(self.__engine.api_client)

        try:
            self.__logger.debug("create application input %s" % str(self))
            response = api_instance.create_application(
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create application response %s"
                                % str(response))

            print_message("Application %s added" % self.application_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
