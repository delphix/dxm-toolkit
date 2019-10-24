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
# Date    : September 2019


import logging

from time import sleep

from masking_apis.models.async_task import AsyncTask
from masking_apis.apis.async_task_api import AsyncTaskApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine


class DxAsyncTask(AsyncTask):

    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        AsyncTask.__init__(self)
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxApplication object")

    def from_asynctask(self, task):
        """
        Copy properties from application object into DxApplication
        :param app: Application object
        """
        self.__dict__.update(task.__dict__)


    def wait_for_task(self):
        """
        """

        api_instance = AsyncTaskApi(self.__engine.api_client)
        try:
            running = True
            while(running):
                self.__logger.debug("wait async input %s" % str(self))
                response = api_instance.get_async_task(
                    self.async_task_id,
                    _request_timeout=self.__engine.get_timeout())
                self.__logger.debug("wait async response %s"
                                    % str(response))
                if response.status != "RUNNING":
                    running = False
                sleep(1)
                print_message("Waiting for task %s to complete " % self.async_task_id)

            if response.status == "SUCCEEDED":
                print_message("Task finished sucesfully")
                return 0
            else:
                print_error("Task finished with status %s" % response.status)
                return 1
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    # def add(self):
    #     """
    #     Add application to Masking engine and print status message
    #     return a None if non error
    #     return 1 in case of error
    #     """

    #     if (self.application_name is None):
    #         print "Application name is required"
    #         self.__logger.error("Application name is required")
    #         return 1

    #     api_instance = ApplicationApi(self.__engine.api_client)

    #     try:
    #         self.__logger.debug("create application input %s" % str(self))
    #         response = api_instance.create_application(
    #             self,
    #             _request_timeout=self.__engine.get_timeout())
    #         self.__logger.debug("create application response %s"
    #                             % str(response))

    #         print_message("Application %s added" % self.application_name)
    #     except ApiException as e:
    #         print_error(e.body)
    #         self.__logger.error(e)
    #         return 1
