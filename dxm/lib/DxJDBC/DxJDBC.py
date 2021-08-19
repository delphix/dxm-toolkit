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

class DxJDBC(object):


    swagger_types = {
        'jdbc_driver_id': 'int',
        'driver_name': 'str',
        'driver_class_name': 'str',
        'description': 'str',
        'version': 'str',
        'uploaded_by': 'str',
        'upload_date': 'datetime',
        'checksum': 'str',
        'built_in': 'bool',
        'logger_installed': 'bool',
        'file_reference_id': 'str',
        'driver_support_id': 'int'
    }

    swagger_map = {
        'jdbc_driver_id': 'jdbcDriverId',
        'driver_name': 'driverName',
        'driver_class_name': 'driverClassName',
        'description': 'description',
        'version': 'version',
        'uploaded_by': 'uploadedBy',
        'upload_date': 'uploadDate',
        'checksum': 'checksum',
        'built_in': 'builtIn',
        'logger_installed': 'loggerInstalled',
        'file_reference_id': 'fileReferenceId',
        'driver_support_id': 'driverSupportId'
    }

    def __init__(self, engine):
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxFileFormat object")

        self.__api = JdbcDriverApi
        self.__apiexc = ApiException
        self.__obj = None

    def from_driver(self, driver):
        self.__obj = driver
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map


    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def jdbc_driver_id(self):
        if self.obj is not None and hasattr(self.obj,'jdbc_driver_id'):
            return self.__obj.jdbc_driver_id
        else:
            return None

    @jdbc_driver_id.setter
    def jdbc_driver_id(self, jdbc_driver_id):
        if self.obj is not None:
            self.obj.jdbc_driver_id = jdbc_driver_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def driver_name(self):
        if self.obj is not None and hasattr(self.obj,'driver_name'):
            return self.__obj.driver_name
        else:
            return None

    @driver_name.setter
    def driver_name(self, driver_name):
        if self.obj is not None:
            self.obj.driver_name = driver_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def driver_class_name(self):
        if self.obj is not None and hasattr(self.obj,'driver_class_name'):
            return self.__obj.driver_class_name
        else:
            return None

    @driver_class_name.setter
    def driver_class_name(self, driver_class_name):
        if self.obj is not None:
            self.obj.driver_class_name = driver_class_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def description(self):
        if self.obj is not None and hasattr(self.obj,'description'):
            return self.__obj.description
        else:
            return None

    @description.setter
    def description(self, description):
        if self.obj is not None:
            self.obj.description = description
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def version(self):
        if self.obj is not None and hasattr(self.obj,'version'):
            return self.__obj.version
        else:
            return None

    @version.setter
    def version(self, version):
        if self.obj is not None:
            self.obj.version = version
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def uploaded_by(self):
        if self.obj is not None and hasattr(self.obj,'uploaded_by'):
            return self.__obj.uploaded_by
        else:
            return None

    @uploaded_by.setter
    def uploaded_by(self, uploaded_by):
        if self.obj is not None:
            self.obj.uploaded_by = uploaded_by
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def upload_date(self):
        if self.obj is not None and hasattr(self.obj,'upload_date'):
            return self.__obj.upload_date
        else:
            return None

    @upload_date.setter
    def upload_date(self, upload_date):
        if self.obj is not None:
            self.obj.upload_date = upload_date
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def checksum(self):
        if self.obj is not None and hasattr(self.obj,'checksum'):
            return self.__obj.checksum
        else:
            return None

    @checksum.setter
    def checksum(self, checksum):
        if self.obj is not None:
            self.obj.checksum = checksum
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def built_in(self):
        if self.obj is not None and hasattr(self.obj,'built_in'):
            return self.__obj.built_in
        else:
            return None

    @built_in.setter
    def built_in(self, built_in):
        if self.obj is not None:
            self.obj.built_in = built_in
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def logger_installed(self):
        if self.obj is not None and hasattr(self.obj,'logger_installed'):
            return self.__obj.logger_installed
        else:
            return None

    @logger_installed.setter
    def logger_installed(self, logger_installed):
        if self.obj is not None:
            self.obj.logger_installed = logger_installed
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def file_reference_id(self):
        if self.obj is not None and hasattr(self.obj,'file_reference_id'):
            return self.__obj.file_reference_id
        else:
            return None

    @file_reference_id.setter
    def file_reference_id(self, file_reference_id):
        if self.obj is not None:
            self.obj.file_reference_id = file_reference_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def driver_support_id(self):
        if self.obj is not None and hasattr(self.obj,'driver_support_id'):
            return self.__obj.driver_support_id
        else:
            return None

    @driver_support_id.setter
    def driver_support_id(self, driver_support_id):
        if self.obj is not None:
            self.obj.driver_support_id = driver_support_id
        else:
            raise ValueError("Object needs to be initialized first")


    def create_driver(self, driver_name, driver_class_name, file_reference_id):
        """
        Create an JDBC driver object
        """  

        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
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
