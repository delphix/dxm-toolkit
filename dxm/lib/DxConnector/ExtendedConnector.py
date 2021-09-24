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
# Comments: List of the Database connectors


import logging
from dxm.lib.DxConnector.DxConnector import DxConnector
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxJDBC.DxJDBCList import DxJDBCList

class ExtendedConnector(DxConnector):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DxConnector.__init__(self, engine)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating ExtendedConnector object")
        self.__jdbclist = DxJDBCList()


    def get_type_properties(self):
        """
        Return dict with properties specific for connector type
        """

        driver_obj = self.__jdbclist.get_by_ref(self.jdbc_driver_id)
        if driver_obj is None:
            driver_name = driver_obj.jdbc_driver_id
        else:
            driver_name = driver_obj.driver_name

        props = {
            'username': self.username,
            'jdbc_driver_name': driver_name,
            'jdbc': self.jdbc
        }
        return props

    def get_properties(self):
        """
        Return dict with properties required for connector type
        """

        props = {
            'jdbc': self.jdbc,
            'username': self.username,
            'schema_name': self.schema_name,
            'connector_name': self.connector_name,
            'password': self.password,
            'database_type': self.database_type,
            'environment_id': self.environment_id,
            'jdbc_driver_id': self.jdbc_driver_id
        }

        empty = 0
        for k in props.keys():
            if (props[k] is None):
                print_error("Property %s can't be empty" % k)
                empty = empty + 1

        if empty == 0:
            return props
        else:
            return None
