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


from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.masking_api.api.async_task_api import AsyncTaskApi
from dxm.lib.masking_api.rest import ApiException

class DxAsyncTask(object):

    swagger_types = {
        'async_task_id': 'int',
        'operation': 'str',
        'reference': 'str',
        'status': 'str',
        'start_time': 'datetime',
        'end_time': 'datetime',
        'cancellable': 'bool'
    }

    swagger_map = {
        'async_task_id': 'asyncTaskId',
        'operation': 'operation',
        'reference': 'reference',
        'status': 'status',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'cancellable': 'cancellable'
    }

    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #AsyncTask.__init__(self)
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxAsyncTask object")

        self.__api = AsyncTaskApi
        self.__obj = None
        self.__apiexc = ApiException
    

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None


    def load_obj(self, task):
        """
        Set a obj property using a AsyncTask
        :param con: DatabaseConnector object
        """
        self.__obj = task
        self.__obj.swagger_map = self.swagger_map
        self.__obj.swagger_types = self.swagger_types

    def wait_for_task(self):
        """
        """

        api_instance = self.__api(self.__engine.api_client)
        try:
            running = True
            while(running):
                self.__logger.debug("wait async input %s" % str(self))
                response = api_instance.get_async_task(
                    self.obj.async_task_id,
                    _request_timeout=self.__engine.get_timeout())
                self.__logger.debug("wait async response %s"
                                    % str(response))
                if response.status != "RUNNING":
                    running = False
                sleep(1)
                print_message("Waiting for task %s to complete " % self.obj.async_task_id)

            if response.status == "SUCCEEDED":
                print_message("Task finished sucesfully")
                return 0
            else:
                print_error("Task finished with status %s" % response.status)
                return 1
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1



