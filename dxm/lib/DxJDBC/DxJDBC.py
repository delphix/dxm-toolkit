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
# Date    : August 2021


import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

from dxm.lib.masking_api.api.jdbc_driver_api import JdbcDriverApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxJDBC.jdbcdriver_mixin import JdbcDriver_mixin

class DxJDBC(JdbcDriver_mixin):


    def __init__(self, engine):
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileFormat object")

        self.__api = JdbcDriverApi
        self.__apiexc = ApiException
        self._obj = None

    def from_driver(self, driver):
        self._obj = driver
        self._obj.swagger_types = self.swagger_types
        self._obj.swagger_map = self.swagger_map



    def create_driver(self, driver_name, driver_class_name, file_reference_id):
        """
        Create an JDBC driver object
        """  

        self._obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.driver_name = driver_name
        self.obj.driver_class_name = driver_class_name
        self.obj.file_reference_id = file_reference_id


    def add(self):

        if (self.obj.driver_name is None):
            print_error("Driver name is required")
            self.__logger.error("Driver name is required")
            return 1

        if (self.obj.driver_class_name is None):
            print_error("Driver class name is required")
            self.__logger.error("Driver class name is required")
            return 1

        try:
            self.__logger.debug("create driver input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_jdbc_driver(body=self.obj)
            self.from_driver(response)

            self.__logger.debug("driver response %s"
                                % str(response))

            print_message("Driver {} added".format(self.obj.driver_name))
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete driver from engine
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete driver id %s"
                                % self.obj.jdbc_driver_id)
            response = api_instance.delete_jdbc_driver(self.obj.jdbc_driver_id)
            self.__logger.debug("delete driver response %s"
                                % str(response))
            print_message("driver %s deleted" % self.obj.driver_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
